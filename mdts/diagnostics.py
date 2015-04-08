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

from datetime import datetime
import logging
import fixtures
import re
import subprocess
from testtools.content import text_content

LOG = logging.getLogger(__name__)


class LogExtractor(fixtures.Fixture):

    def __init__(self, test, log_files):
        self.test = test
        self.log_files = log_files
        self.marker_id = \
            test.id() + datetime.now().strftime(' %Y-%m-%d %H:%M:%S')
        self.markers = self.get_markers()
        test.addOnException(self.cleanUpOnException)

    def setUp(self):
        super(LogExtractor, self).setUp()
        self._add_marker(self.markers['start'])

    def cleanUpOnException(self, exc_info):
        self._add_marker(self.markers['end'])
        cmdline = 'sed -n "/%s/, /%s/ p" %s'
        for log_file in self.log_files:
            log_content = subprocess.check_output(
                cmdline % (self.markers['start'],
                           self.markers['end'],
                           log_file),
                shell=True)
            self.test.addDetail(log_file, text_content(log_content))

    def get_markers(self, escape=True):
        if escape:
            marker_id = re.escape(self.marker_id)
        else:
            marker_id = self.marker_id
        start = "---- START %s" % marker_id
        end = "---- END %s" % marker_id
        return {'start': start, 'end': end}

    def _add_marker(self, marker):
        cmdline = "echo %s >> %s"
        for log_file in self.log_files:
            subprocess.check_output(cmdline % (marker, log_file), shell=True)
