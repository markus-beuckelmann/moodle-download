moodle-download
=======

_moodle-dowload.py_ is a small Python script to download a set of specifed files from the [Moodle](http://moodle.org/) e-learning platform. You can create profiles (simple [JSON](http://en.wikipedia.org/wiki/JSON) files) that provide information on the courses and use [regular expressions](http://en.wikipedia.org/wiki/Regular_expression) to determine which files should be downloaded and where they belong.

So far this has only been tested with the [e-learning platform](http://elearning2.uni-heidelberg.de) (v2.9) at University of Heidelberg. In principle, this could work for other Moodle platforms as well, but some modifications might be necessary.

If you want to check for new files and download them automatically, just set up a cron job or use a systemd service that runs `moodle-download.py` periodically.

Installation
------------

1. Download or clone the repository from GitHub.
2. Install the requirements: `sudo pip install -r requirements.txt`
3. Create necessary directories: `mkdir -p ~/.config/moodle-download/profiles`
4. Copy your configuration file to `~/.config/moodle-download/moodle-download.conf` (see `moodle-download.conf.example` for an example)
5. Put your profile files in `profiles/` (see `WS-2015-2016.example` for an example)
6. Optional: Set up a cron job or a systemd service.

Profiles
------------

All profile files must be valid JSON files. For every course you take, add a new dictionary to the profile. The key should be the course title (but doesn't really matter), `id` is the Moodle course id (see URL of overview page), `short` is a short description that will be used for symlinks, and `downloads` lists the files to download. The first element is a regular expression that should match the files to download, second specifies the rename pattern and the third determines the download location.

Requirements
------------

Please install the following Python packages: [docopt](https://pypi.python.org/pypi/docopt), [mechanize](https://pypi.python.org/pypi/mechanize/), [dbus-python](https://pypi.python.org/pypi/dbus-python/). You can do that by running:

`sudo pip install -r requirements.txt`

License
-------

**GNU General Public License (GPLv3)**, see `LICENSE.txt` for further details.
