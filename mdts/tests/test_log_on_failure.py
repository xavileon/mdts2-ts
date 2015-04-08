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

from mdts import test
import tempfile
import subprocess
from testtools.matchers import DocTestMatches


class LogFailureTest(test.MDTSBaseTest):
    class ReferenceTest(test.MDTSBaseTest):
        def setUp(self):
            self.files_to_log = []
            self.files_to_log.append(tempfile.NamedTemporaryFile().name)
            self.files_to_log.append(tempfile.NamedTemporaryFile().name)
            for log_file in self.files_to_log:
                subprocess.check_output(
                    "echo 'OUTSIDE TEST' > %s" % log_file,
                    shell=True)
            super(LogFailureTest.ReferenceTest, self).setUp()

        def test_log_on_failure(self):
            for log_file in self.files_to_log:
                subprocess.check_output(
                    "echo 'INSIDE TEST' >> %s" % log_file,
                    shell=True)
            raise Exception()

        def test_no_log_on_pass(self):
            for log_file in self.files_to_log:
                subprocess.check_output(
                    "echo 'INSIDE TEST' >> %s" % log_file,
                    shell=True)

    def setUp(self):
        self.files_to_log = []
        super(LogFailureTest, self).setUp()

    def test_log_on_failure(self):
        ref_test = LogFailureTest.ReferenceTest('test_log_on_failure')
        ref_test.run()
        ref_markers = ref_test.diagnose.get_markers(escape=False)
        exc_details = ref_test.getDetails()
        for log_file in ref_test.files_to_log:
            self.assertThat(
                exc_details[log_file].as_text(),
                DocTestMatches(
                    "%s\nINSIDE TEST\n%s\n" % (ref_markers['start'],
                                               ref_markers['end'])))

    def test_no_log_on_pass(self):
        ref_test = self.ReferenceTest('test_no_log_on_pass')
        ref_test.run()
        exc_details = ref_test.getDetails()
        for log_file in ref_test.files_to_log:
            self.assertNotIn(log_file, exc_details.keys())
