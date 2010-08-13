=======================================
mcgrep - Grep through memcached servers
=======================================

:Authors:
    Scott Torborg (storborg)
:Version: 0.1

A simple tool to grep through memcached. Uses the poorly-documented features outlined in the the 2010 Black Hat presentation by SensePost:

http://www.sensepost.com/blog/4873.html

*Note* Use at your own risk!


Installation
============

Simple as::

    $ easy_install mcgrep

Or if you prefer, download the source and then::

    $ python setup.py build
    $ python setup.py install

Installing the package installs both the mcgrep python module and the mcgrep
command-line utility.


License
=======

mcgrep is released under the GNU General Public License (GPL). See the LICENSE file for full text of the license.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
