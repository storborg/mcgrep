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


Example
=======

First let's set some keys::

    $ telnet localhost 11211
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    set quux 0 0 7
    boogie!
    STORED
    quit
    Connection closed by foreign host.

mcgrep defaults to connecting to a localhost memcached instance::

    $ mcgrep boogie
    quux

Or you can specify servers::

    $ mcgrep -s foo.example.com:11211 -s bar.example.com boogie
    quux

Specify -V to print values as well::

    $ mcgrep -V oogie
    quux:'boogie!'

Or no pattern to just dump all keys::

    $ mcgrep
    quux


License
=======

mcgrep is released under the GNU General Public License (GPL). See the LICENSE file for full text of the license.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
