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

import logging
from testtools import testcase
from mdts import diagnostics

LOG = logging.getLogger(__name__)


class MDTSBaseTest(testcase.WithAttributes,
                   testcase.TestCase):

    def setUp(self):
        super(MDTSBaseTest, self).setUp()
        # FIXME: change it by the files provided by PTM
        # TODO: check if the files pulled exist
        mdts_files_to_log = \
            ['/opt/stack/logs/screen-midolman.log',
             '/opt/stack/logs/screen-midonet-api.log',
             '/var/log/zookeeper/zookeeper.log',
             '/var/log/cassandra/system.log']
        # Test specific files to log (defined on base_class)
        if hasattr(self, 'files_to_log'):
            mdts_files_to_log = self.files_to_log
        self.diagnose = self.useFixture(
            diagnostics.LogExtractor(self, mdts_files_to_log))
