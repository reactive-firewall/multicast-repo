#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Multicast Python Module (Testing)
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://www.github.com/reactive-firewall/multicast/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__module__ = """tests"""

try:
	"""Handle imports with CWE-758 mitigation.

	This implementation uses a nested try-except pattern to:
	1. Attempt direct context import
	2. Fallback to relative import
	3. Validate context module integrity
	4. Import required dependencies

	References:
	- CWE-758: Reliance on Undefined, Unspecified, or Implementation-Defined Behavior
	"""
	try:
		import context
	except Exception as ImportErr:  # pragma: no branch
		ImportErr = None
		del ImportErr  # skipcq - cleanup any error leaks early
		from . import context
	if context.__name__ is None:
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import sys
		from context import unittest
		from context import subprocess
		import signal
		import time
		from context import BasicUsageTestSuite
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


class TestHearKeyboardInterrupt(BasicUsageTestSuite):
	"""
	Test suite for verifying keyboard interrupt (SIGINT) handling.

	This suite ensures that the multicast service properly handles
	SIGINT signals by cleaning up resources and exiting gracefully
	with the expected status code (130).
	"""
	__module__ = """tests.test_hear_keyboard_interrupt"""

	def test_hear_keyboard_interrupt(self):
		"""Tests the special hear and stop test"""
		theResult = False
		fail_fixture = str("""C^INT --> HEAR == error""")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_cmd = str("{} -m coverage run -p --context=Integration").format(sys.executable)
			_fixture_HEAR_args = [
				_fixture_cmd, """--source=multicast""",
				"""-m""", """multicast""",
				"""--daemon""", """HEAR""",
				"""--port""", str(_fixture_port_num),
				"""--group""", """224.0.0.1"""
			]
			self.assertIsNotNone(_fixture_HEAR_args)
			process = subprocess.Popen(
				context.checkCovCommand(*_fixture_HEAR_args),
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True
			)
			try:
				time.sleep(1)  # Allow server to start
				process.send_signal(signal.SIGINT)
				stdout, stderr = process.communicate(timeout=5)
				self.assertIsNotNone(stdout, "Incomplete Test.")
				self.assertIsNotNone(stderr, "Incomplete Test.")
				self.assertIsNotNone(process.returncode, "Incomplete Test.")
				self.assertNotEqual(int(process.returncode), int(2), "Invalid Test Arguments.")
				self.assertEqual(int(process.returncode), int(130), "CEP-8 VIOLATION.")
				theResult = (int(process.returncode) >= int(1))
			finally:
				process.kill()
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


# leave this part
if __name__ == '__main__':
	unittest.main()
