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


class ConditionalExecutionsTest(test.MDTSBaseTest):

    class ReferenceTest(test.MDTSBaseTest):
        def setUp(self):
            self.files_to_log = []
            super(ConditionalExecutionsTest.ReferenceTest, self).setUp()

        @decorators.expected_failure("JIRA-1")
        def test_expected_failure_and_fail(self):
            raise Exception("Test failed for an expected reason, should pass")

        @decorators.expected_failure("JIRA-1")
        def test_expected_failure_and_pass(self):
            pass

        @decorators.intermittent_failure("JIRA-2")
        def test_intermittent_failure_and_fail(self):
            msg = "Test failed for an intermittent reason, should pass"
            raise Exception(msg)

        @decorators.intermittent_failure("JIRA-2")
        def test_intermittent_failure_and_pass(self):
            pass

        @decorators.feature_not_implemented("JIRA-3")
        def test_feature_not_implemented_fail(self):
            raise Exception("Feature not implemented yet")

        @decorators.feature_not_implemented("JIRA-3")
        def test_feature_not_implemented_pass(self):
            # The feature "pass" has been implemented
            pass

    def setUp(self):
        self.files_to_log = []
        super(ConditionalExecutionsTest, self).setUp()

    def test_expected_failure_and_fail(self):
        ref_test_name = "test_expected_failure_and_fail"
        ref_test = ConditionalExecutionsTest.ReferenceTest(ref_test_name)
        ref_result = ref_test.run()
        self.assertIs(True, ref_result.wasSuccessful())
        self.assertIn("expected_failure", ref_test.id())

    def test_expected_failure_but_pass(self):
        ref_test_name = "test_expected_failure_and_pass"
        ref_test = ConditionalExecutionsTest.ReferenceTest(ref_test_name)
        ref_test.run()
        exc_details = ref_test.getDetails()
        self.assertThat(
            exc_details['traceback'].as_text(),
            DocTestMatches("...EXPECTED FAILURE (status=PASS)...",
                           doctest.ELLIPSIS))
        self.assertIn("expected_failure", ref_test.id())

    def test_intermittent_failure_and_pass(self):
        ref_test_name = "test_intermittent_failure_and_pass"
        ref_test = ConditionalExecutionsTest.ReferenceTest(ref_test_name)
        ref_result = ref_test.run()
        self.assertIs(True, ref_result.wasSuccessful())
        self.assertIn("intermittent_failure", ref_test.id())

    def test_intermittent_failure_and_fail(self):
        ref_test_name = "test_intermittent_failure_and_fail"
        ref_test = ConditionalExecutionsTest.ReferenceTest(ref_test_name)
        ref_result = ref_test.run()
        self.assertIs(True, ref_result.wasSuccessful())
        self.assertIn("intermittent_failure", ref_test.id())

    def test_feature_not_implemented_fail(self):
        ref_test_name = "test_feature_not_implemented_fail"
        ref_test = ConditionalExecutionsTest.ReferenceTest(ref_test_name)
        ref_result = ref_test.run()
        self.assertIs(True, ref_result.wasSuccessful())
        self.assertIn("feature_not_implemented", ref_test.id())

    def test_feature_not_implemented_pass(self):
        ref_test_name = "test_feature_not_implemented_pass"
        ref_test = ConditionalExecutionsTest.ReferenceTest(ref_test_name)
        ref_result = ref_test.run()
        self.assertIs(True, ref_result.wasSuccessful())
        self.assertIn("feature_not_implemented", ref_test.id())
