# Copyright 2015 Midokura SARL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import doctest
from mdts import test
from mdts import decorators
from testtools.matchers import DocTestMatches
#from testtools.testcase import attr
from nose.plugins.attrib import attr

class AttributeSelectionTest(test.MDTSBaseTest):

    def setUp(self):
        self.files_to_log = []
        super(AttributeSelectionTest, self).setUp()

    @attr(type="smoke")
    def test_smoke_test(self):
        pass
