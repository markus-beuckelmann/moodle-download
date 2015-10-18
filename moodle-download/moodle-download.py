#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

'''
Usage:
	moodle-download.py <profile>
	moodle-download.py (-h | --help | --version)

Options:
	-h, --help	Shows the help screen.
	-v, --version	Prints the version and exits.
'''

__author__ = 'Markus Beuckelmann'
__author_email__ = 'email@markus-beuckelmann.de'
__version__ = '0.1.0'

import os
import sys
import json
import re
import mechanize

from docopt import docopt
from getpass import getpass
from cookielib import LWPCookieJar as cookiejar

from helpers import *

CONFIGPATH = os.path.join(os.getenv('HOME'), '.config', 'moodle-download', 'moodle-download.conf')
PROFILEPATH = os.path.join(os.path.dirname(CONFIGPATH), 'profiles')
REFLAGS = re.IGNORECASE | re.UNICODE

args = docopt(__doc__, version = __version__)

if not os.path.exists(args['<profile>']) and not os.path.exists(os.path.join(PROFILEPATH, args['<profile>'])):
	sys.exit('Profile "%s" not found. Quitting.' % args['<profile>'])
else:
	path = args['<profile>'] if os.path.exists(args['<profile>']) else os.path.join(PROFILEPATH, args['<profile>'])

try:
	courses = json.load(open(path, 'r'))
except ValueError:
	sys.exit('"%s" is not a valid JSON file. Quitting.' % path)

if os.path.exists(CONFIGPATH):
	try:
		config = json.loads(open(CONFIGPATH, 'r').read())
	except ValueError:
		sys.exit('"%s" is not a valid JSON file. Quitting.' % CONFIGPATH.replace(os.getenv('HOME'), '~'))
else:
	sys.exit('Please create a configuration file at "%s". Quitting.' % configpath.replace(os.getenv('HOME'), '~'))

if not config.has_key('password') or not config['password']:
	config['password'] = getpass('Password: ')

urls = {'baseurl' : 'https://%s' % config['server']}
urls.update({'login' : '%s/login/index.php' % urls['baseurl'], 'overview' : '%s/course/view.php?id={ID}' % urls['baseurl']})
blacklist = []

browser = mechanize.Browser()
cookies = cookiejar()
browser.set_cookiejar(cookies)
if config.has_key('user-agent') and config['user-agent']:
	browser.addheaders = [('User-agent', config['user-agent'])]

# This could be helpful for debugging...
# browser.set_debug_http(True)
# browser.set_debug_redirects(True)
# browser.set_debug_responses(True)

login(browser, urls['login'], config)
print 'Login successful (%s@%s).' % (config['username'], config['server'])

for course in courses.iterkeys():

	content = browser.open(urls['overview'].replace('{ID}', str(courses[course]['id'])))
	html = content.read()

	for link in browser.links():

		if not '/mod/resource/' in link.url:
			continue

		#description = link.text
		#for string in [' File', ' Datei', 'File[IMG]', 'Datei[IMG]', '[IMG]']:
		#	description = description.replace(string, '').strip()

		sublink = browser.open(link.url).geturl()
		for download in courses[course]['downloads']:

			filename = os.path.basename(sublink)
			if re.search(download[0], filename, REFLAGS):

				if config.has_key('pad-with-zeros') and config['pad-with-zeros'] > 0:
					localname = download[1].replace('{#}', re.search(download[0], filename, REFLAGS).groups()[0].zfill(config['pad-with-zeros']))
				else:
					localname = download[1].replace('{#}', re.search(download[0], filename, REFLAGS).groups()[0])

				src, dest = sublink, os.path.join(os.path.expanduser(download[2]), localname)

				if src in blacklist:
					continue

				if not os.path.exists(dest):

					if courses[course].has_key('username') and courses[course].has_key('password'):
						browser.add_password(src, courses[course]['username'], courses[course]['password'])

					if not os.path.exists(os.path.dirname(dest)):
						os.makedirs(os.path.dirname(dest))

					print '%s: Downloading "%s"...' % (course, os.path.basename(dest))
					browser.retrieve(src, filename = dest)

					if config['desktop-notifications']:
						summary, body = u'%s' % course, '%s: %s' % (os.path.basename(dest), config['desktop-notification-text'] if config.has_key('desktop-notification') else 'Download finished')
						notify(summary, body)

					if config.has_key('symlink-on-desktop') and config['symlink-on-desktop']:
						symlinkdest, symlinksrc = dest, '%s/Desktop/%s-%s' % (os.getenv('HOME'), courses[course]['short'], os.path.basename(dest))
						if not os.path.exists(symlinksrc):
							print '%s -> %s' % (symlinksrc.replace(os.getenv('HOME'), '~'), symlinkdest.replace(os.getenv('HOME'), '~'))
							os.symlink(symlinkdest, symlinksrc)

				else:
					print '%s: "%s" already exists.' % (course, os.path.basename(dest))

				blacklist.append(src)
