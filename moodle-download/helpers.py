#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

__all__ = ['login', 'LoginException']

class LoginException(Exception):
	pass

def login(browser, url, config):
	''' Performs the login procedure using specified username and password. '''

	content = browser.open(url)
	html = content.read()

	try:
		browser.select_form(nr = [form.attrs.get('id') for form in browser.forms()].index('login'))
	except ValueError:
		raise LoginException('There is no login form to select.')

	if not (config.has_key('username') and config['username']) or not (config.has_key('password') and config['password']):
		raise LoginException('You need to specify a username and password.')

	browser.form['username'] = config['username']
	browser.form['password'] = config['password']
	browser.submit()

	if not [element.text for element in browser.links() if element.text == 'Logout']:
		raise LoginException('Something went wrong. Is your username/password correct?')
