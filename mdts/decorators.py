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


import functools
import logging
from testtools.testcase import attr
import traceback

LOG = logging.getLogger(__name__)
LOG = logging.getLogger("notification")


def intermittent_failure(issue):
    """
    If test PASS | FAIL -> OK, indicate an intermittent failure reported by
    the issue.
    """
    def decorator(test_func):
        @attr('intermittent_failure(%s)' % issue)
        @functools.wraps(test_func)
        def wrapper(self, *func_args, **func_kwargs):
            try:
                test_func(self, *func_args, **func_kwargs)
            except Exception:
                exc_info = traceback.format_exc()
                # TODO: may be necessary to report also the log file details
                LOG.info("\n=========================================\n" +
                         "INTERMITTENT FAILURE (status=FAIL) [%s] " % issue +
                         "in %s\n" % self.id() +
                         "-----------------------------------------\n" +
                         "%s" % exc_info +
                         "-----------------------------------------\n")
            else:
                LOG.info("\n=========================================\n" +
                         "INTERMITTENT FAILURE (status=PASS) [%s] " % issue +
                         "in %s\n" % self.id() +
                         "-----------------------------------------\n")
        return wrapper
    return decorator


def expected_failure(issue):
    """
    If test PASS -> FAIL, indicate a failure with a notification
    to change the conditional validation of the test back to normal.
    If test FAIL -> OK, indicate a pass with a notification
    that this test is expected to fail according to the JIRA issue
    """
    def decorator(test_func):
        @attr('expected_failure(%s)' % issue)
        @functools.wraps(test_func)
        def wrapper(self, *func_args, **func_kwargs):
            try:
                test_func(self, *func_args, **func_kwargs)
            except Exception:
                exc_info = traceback.format_exc()
                # TODO: may be necessary to report also the log file details
                LOG.info("\n=========================================\n" +
                         "EXPECTED FAILURE (status=FAIL) [%s] " % issue +
                         " in %s\n" % self.id() +
                         "-----------------------------------------\n" +
                         "%s" % exc_info +
                         "-----------------------------------------\n")
            else:
                raise Exception("EXPECTED FAILURE (status=PASS) [%s]" % issue +
                                " in %s. " % self.id() +
                                "Issue resolved. " +
                                "Remove the expected_failure decorator")
        return wrapper
    return decorator


def feature_not_implemented(issue):
    """
    If test PASS -> OK, indicate a pass with a notification
    to change the conditional validation of the test back to normal.
    If test FAIL -> OK, the results indicate a pass with a notification
    that this test does not yet implement a given feature pointed
    by the issue
    """
    def decorator(test_func):
        @attr('feature_not_implemented(%s)' % issue)
        @functools.wraps(test_func)
        def wrapper(self, *func_args, **func_kwargs):
            try:
                test_func(self, *func_args, **func_kwargs)
            except Exception:
                LOG.info("\n=========================================\n" +
                         "FEATURE in %s NOT IMPLEMENTED " % issue +
                         "in test %s\n" % self.id() +
                         "-----------------------------------------\n")
            else:
                LOG.info("\n=========================================\n" +
                         "FEATURE in %s ALREADY IMPLEMENTED. " % issue +
                         "Change the status of test %s " % self.id() +
                         "back to 'normal'\n" +
                         "-----------------------------------------\n")
        return wrapper
    return decorator
