vsmtpd
======

About
-----
After using qpsmtpd for some time and finding that its design was very
flexible and very well put together. This has spawned from the vmail project
which is mostly written in Python.

Wanting to experiment at how well TwistedMail could perform accepting
connections, as the majority of time spent during a SMTP conversation is
out of qpsmtpd (network i/o, spam scanning, virus checking), it seemed that
an async model rather than fork model would be preferable in terms of
memory consumption on inbound servers. Although qpsmtpd has an async model
not all the plugins are functional on it from what I could gather.

After an initial effort of using Twisted however, it became apparent that
Twisted's SMTP implementation wasn't suited for the sort of SMTP server
vsmtpd is aspiring to be, so the core was switched to using gevent which
allows for a very efficient server.

Installation
------------
The same as any Python project::

	python setup.py build
	python setup.py install

Configuration
-------------
Configuration is fairly simple, just uses a basic ini file format. There
is an example configuration file bundled with the source, as well as a
bundled logging configuration file. The logging framework within vsmtpd
is simply the built-in logging for Python, so any log handlers can simply
be added from this file.

Plugins
-------
Wanting to mimick how qpsmtpd is put together, the core of vsmtpd does very
little and denies mail to all recipients by default. The
functionality to accept messages, authenticate etc. will all come
from plugins that subscribe to hooks. See the docs/hooks.rst document for
details on what these hooks do.
