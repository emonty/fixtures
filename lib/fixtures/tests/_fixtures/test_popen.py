#  fixtures: Fixtures with cleanups for testing and convenience.
#
# Copyright (c) 2010, Robert Collins <robertc@robertcollins.net>
# 
# Licensed under either the Apache License, Version 2.0 or the BSD 3-clause
# license at the users choice. A copy of both licenses are available in the
# project source as Apache-2.0 and BSD. You may not use this file except in
# compliance with one of these two licences.
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under these licenses is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# license you chose for the specific language governing permissions and
# limitations under that license.

import subprocess

import testtools
from testtools.compat import (
    _b,
    BytesIO,
    )

import fixtures
from fixtures import PopenFixture, TestWithFixtures
from fixtures._fixtures.popen import FakeProcess


class TestPopenFixture(testtools.TestCase, TestWithFixtures):

    def test_installs_restores_global(self):
        fixture = PopenFixture()
        popen = subprocess.Popen
        fixture.setUp()
        try:
            self.assertEqual(subprocess.Popen, fixture)
        finally:
            fixture.cleanUp()
            self.assertEqual(subprocess.Popen, popen)

    def test___call___is_recorded(self):
        fixture = self.useFixture(PopenFixture())
        proc = fixture(['foo', 'bar'], 1, None, 'in', 'out', 'err')
        self.assertEqual(1, len(fixture.procs))
        self.assertEqual(dict(args=['foo', 'bar'], bufsize=1, executable=None,
            stdin='in', stdout='out', stderr='err'), proc._args)

    def test_inject_content_stdout(self):
        def get_info(args):
            return {'stdout': 'stdout'}
        fixture = self.useFixture(PopenFixture(get_info))
        proc = fixture(['foo'])
        self.assertEqual('stdout', proc.stdout)


class TestFakeProcess(testtools.TestCase):

    def test_wait(self):
        proc = FakeProcess({}, {})
        proc.returncode = 45
        self.assertEqual(45, proc.wait())

    def test_communicate(self):
        proc = FakeProcess({}, {})
        self.assertEqual(('', ''), proc.communicate())
        self.assertEqual(0, proc.returncode)

    def test_communicate_with_out(self):
        proc = FakeProcess({}, {'stdout': BytesIO(_b('foo'))})
        self.assertEqual((_b('foo'), ''), proc.communicate())
        self.assertEqual(0, proc.returncode)
