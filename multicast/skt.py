#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Multicast Repo
# ..................................
# Copyright (c) 2017-2024, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/python-repo/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Third-party Acknowledgement:
# ..........................................
# Some code (namely: run, and parseArgs) was modified/derived from:
# https://stackoverflow.com/a/52791404
# Copyright (c) 2019, "pterodragon" (https://stackoverflow.com/users/5256940/pterodragon)
# which was under CC-by-sa-4 license.
# see https://creativecommons.org/licenses/by-sa/4.0/ for details
# The components in parseArgs, run, and main are thus also under
# CC-by-sa-4 https://creativecommons.org/licenses/by-sa/4.0/
# ..........................................
# NO ASSOCIATION

"""Socket utility functions for multicast communication.

Provides helper functions for creating and managing multicast sockets.

NOT intended for DIRECT use!

Caution: See details regarding dynamic imports [documented](../__init__.py) in this module.

Minimal Acceptance Testing:

First set up test fixtures by importing multicast.

Testcase 0: Multicast should be importable.

	>>> import multicast
	>>> multicast.skt is not None
	True
	>>> multicast.skt.__doc__ is not None
	True
	>>>

Testcase 1: SKT utils should be automatically imported.
	A: Test that the multicast.skt component is initialized.
	B: Test that the skt component is initialized.
	C: Test that the skt component has __doc__

	>>> multicast is not None
	True
	>>> multicast.skt is not None
	True
	>>> multicast.skt.__doc__ is not None
	True
	>>> type(multicast.skt.__doc__) == type(str(''''''))
	True
	>>>

Testcase 2: SKT utils should be detailed with some metadata.
	A: Test that the __MAGIC__ variables are initialized.
	B: Test that the __MAGIC__ variables are strings.

	>>> multicast.skt is not None
	True
	>>> multicast.skt.__module__ is not None
	True
	>>> multicast.skt.__package__ is not None
	True
	>>> type(multicast.skt.__doc__) == type(multicast.skt.__module__)
	True
	>>>


"""


__package__ = """multicast"""  # skipcq: PYL-W0622
"""The package of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: SKT utils should be automatically imported.

		>>> multicast.skt.__package__ is not None
		True
		>>>
		>>> multicast.skt.__package__ == multicast.__package__
		True
		>>>

"""


__module__ = """multicast.skt"""
"""The module of this program.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: SKT utils should be automatically imported.

		>>> multicast.skt.__module__ is not None
		True
		>>>

"""


__file__ = """multicast/skt.py"""
"""The file of this component."""


__name__ = """multicast.skt"""  # skipcq: PYL-W0622
"""The name of this component.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

	Testcase 0: Multicast should be importable.

		>>> import multicast
		>>>

	Testcase 1: SKT utils should be automatically imported.

		>>> multicast.skt.__name__ is not None
		True
		>>>

"""


try:
	from . import socket as _socket  # skipcq: PYL-C0414
	from . import struct as _struct  # noqa
	from . import _MCAST_DEFAULT_TTL as _MCAST_DEFAULT_TTL  # skipcq: PYL-C0414
except Exception as err:
	baton = ImportError(err, str("[CWE-758] Module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = err
	raise baton from err


def genSocket():
	"""
	Create and configure a multicast socket.

	Generates an unbound socket.socket object ready to receive network traffic.
	Implementation allows reuse of socket (to allow another instance of python running
	this script binding to the same ip/port).

	Returns:
		socket.socket: A configured multicast socket ready for communication.

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 0: skt should be automatically imported.
		A: Test that the multicast component is initialized.
		B: Test that the skt component is initialized.

		>>> multicast is not None
		True
		>>> multicast.skt is not None
		True
		>>>

	Testcase 1: skt should have genSocket() function that returns a socket.socket object.
		A: Test that the skt component has the function 'genSocket'
		B: Test that the 'genSocket' function returns a socket

		>>> multicast.skt.genSocket is not None
		True
		>>> multicast.skt.genSocket #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<function genSocket at ...>
		>>> type(multicast.skt.genSocket)
		<class 'function'>
		>>> type(multicast.skt.genSocket())
		<class 'socket.socket'>
		>>>


	"""
	sock = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM, _socket.IPPROTO_UDP)
	sock.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
	sock.settimeout(_MCAST_DEFAULT_TTL)
	return sock


def endSocket(sock=None):
	"""Close a multicast socket and release resources.

	Args:
		sock (socket.socket, optional): The socket to close. Defaults to None.

	Returns:
		None

	Minimal Acceptance Testing:

	First set up test fixtures by importing multicast.

		>>> import multicast
		>>> multicast.__doc__ is not None
		True
		>>>

	Testcase 0: skt should be automatically imported.
		A: Test that the multicast component is initialized.
		B: Test that the skt component is initialized.

		>>> multicast is not None
		True
		>>> multicast.skt is not None
		True
		>>>

	Testcase 1: skt should have endSocket() function that takes a socket.socket and closes it.
		A: Test that the skt component has the function 'genSocket'
		B: Test that the skt component has the function 'endSocket'
		C: Test that the 'endSocket' function returns None when given the genSocket

		>>> multicast.skt.genSocket is not None
		True
		>>> multicast.skt.endSocket is not None
		True
		>>> multicast.skt.endSocket #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<function endSocket at ...>
		>>> type(multicast.skt.endSocket)
		<class 'function'>
		>>> temp_fxtr = multicast.skt.endSocket(multicast.skt.genSocket())
		>>> temp_fxtr is None
		True
		>>>

	Testcase 2: skt should have endSocket() function that takes a socket.socket object,
		otherwise does nothing.
		A: Test that the skt component has the function 'endSocket' (see testcase 1)
		B: Test that the 'endSocket' function returns nothing

		>>> multicast.skt.endSocket is not None
		True
		>>> multicast.skt.endSocket #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		<function endSocket at ...>
		>>> type(multicast.skt.endSocket)
		<class 'function'>
		>>> multicast.skt.endSocket(None) is None
		True
		>>>


	"""
	if sock is not None:  # pragma: no branch
		try:
			try:
				sock.shutdown(_socket.SHUT_RD)  # pragma: no cover
				sock.detach()
			finally:
				sock.close()  # Some systems won't close
		except OSError as err:  # pragma: no branch
			sock = None  # So catch and zero the socket
	if sock:
		raise ResourceWarning()
