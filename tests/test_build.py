#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Multicast PEP-517 Tests
# ..................................
# Copyright (c) 2024, Mr. Walls
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
	except Exception as ImportErr:  # pragma: no branch
		ImportErr = None
		del ImportErr  # skipcq - cleanup any error leaks early
		from . import context
	if context.__name__ is None:
		raise ImportError("[CWE-758] Failed to import context") from None
	else:
		from context import sys
		from context import os
		from context import unittest
		from context import subprocess
		from context import BasicUsageTestSuite
except Exception as _cause:  # pragma: no branch
	raise ImportError("[CWE-758] Failed to import test context") from _cause


class TestPEP517Build(BasicUsageTestSuite):

	__module__ = """tests.test_build"""

	def test_build_with_pep517(self):
		"""Test building the package using PEP 517 standards."""
		# Arguments need to clean
		build_arguments = [
			str("{} -m coverage run").format(sys.executable),
			'setup.py', 'clean', '--all'
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running clean"), str(theBuildtxt))
		# Arguments need to build
		build_arguments = [
			str("{} -m coverage run").format(sys.executable),
			'-m', 'build', '--sdist', '--wheel'
		]
		# Build the source distribution
		theBuildtxt = context.checkPythonCommand(build_arguments, stderr=subprocess.STDOUT)
		self.assertIn(str("running build"), str(theBuildtxt))
		self.assertIn(str("""Successfully built"""), str(theBuildtxt))
		# Verify that the dist directory contains the expected files
		dist_dir = os.path.join(os.getcwd(), 'dist')
		version = self._get_package_version()
		dist_files = sorted(os.listdir(dist_dir), reverse=True)
		expected_files = [
			f"multicast-{version}.tar.gz",
			f"multicast-{version}-py3-none-any.whl",
		]
		for expected_file in expected_files:
			self.assertIn(
				expected_file, dist_files,
				str('Missing {expected} in dist directory. Looking for version {version}').format(
					expected=expected_file, version=version
				)
			)


# leave this part
if __name__ == '__main__':
	unittest.main()
