#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Test Repo Template
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

__module__ = """tests"""


try:
	try:
		import context
	except Exception as _:  # pragma: no branch
		del _  # skipcq - cleanup any error vars early
		from . import context
	if context.__name__ is None:
		raise ModuleNotFoundError("[CWE-758] Failed to import context") from None
	else:
		from context import multicast  # pylint: disable=cyclic-import - skipcq: PYL-R0401
		from context import unittest
		from context import Process
except Exception as err:
	raise ImportError("[CWE-758] Failed to import test context") from err


class HearCleanupTestSuite(context.BasicUsageTestSuite):

	__module__ = """tests.test_hear_cleanup"""

	__name__ = """tests.test_hear_cleanup.HearCleanupTestSuite"""

	def test_cleanup_on_exit(self):
		"""Tests the special hear and stop test"""
		theResult = False
		fail_fixture = str("""STOP --> HEAR == error""")
		_fixture_port_num = self._the_test_port
		try:
			self.assertIsNotNone(_fixture_port_num)
			self.assertEqual(type(_fixture_port_num), type(int(0)))
			_fixture_SAY_args = [
				"""--port""", _fixture_port_num,
				"""--group""", """224.0.0.1""",
				"""--message""", """'STOP Test'"""
			]
			_fixture_HEAR_kwargs = {
				"""port""": _fixture_port_num,
				"""group""": """224.0.0.1"""
			}
			p = Process(
				target=multicast.hear.McastHEAR().doStep,
				name="HEAR", kwargs=_fixture_HEAR_kwargs
			)
			p.start()
			self.assertIsNotNone(p)
			self.assertTrue(p.is_alive())
			try:
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
				)
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
				)
				self.assertIsNotNone(
					multicast.__main__.McastDispatch().doStep("SAY", _fixture_SAY_args)
				)
			except Exception as _cause:
				p.join()
				raise unittest.SkipTest(fail_fixture) from _cause
			p.join()
			self.assertIsNotNone(p.exitcode)
			self.assertEqual(int(p.exitcode), int(0))
			theResult = (int(p.exitcode) <= int(0))
		except Exception as err:
			context.debugtestError(err)
			self.fail(fail_fixture)
			theResult = False
		self.assertTrue(theResult, fail_fixture)


if __name__ == '__main__':
	unittest.main()
