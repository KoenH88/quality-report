"""
Copyright 2012-2016 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from ..abstract import owasp_dependency_report
from .. import url_opener
from ..jenkins import Jenkins


class JenkinsOWASPDependencyReport(owasp_dependency_report.OWASPDependencyReport, Jenkins):
    """ Class representing OWASP dependency reports in Jenkins jobs. """

    def __init__(self, *args, **kwargs):
        super(JenkinsOWASPDependencyReport, self).__init__(*args, **kwargs)
        self.__report_url = self._last_successful_build_url + 'dependency-check-jenkins-pluginResult/'
        self.__report_api_url = self.__report_url + self.api_postfix

    def nr_warnings(self, job_names, priority):
        """ Return the number of warnings in the jobs with the specified priority. """
        assert priority in ('low', 'normal', 'high')
        warnings = [self.__nr_warnings(job_name, priority) for job_name in job_names]
        return -1 if -1 in warnings else sum(warnings)

    def __nr_warnings(self, job_name, priority):
        """ Return the number of warnings of the specified type in the job. """
        job_name = self.resolve_job_name(job_name)
        url = self.__report_api_url.format(job=job_name)
        try:
            report_dict = self._api(url)
        except url_opener.UrlOpener.url_open_exceptions as reason:
            logging.warn("Couldn't open %s to read warning count %s: %s", url, priority, reason)
            return -1
        return int(report_dict['numberOf{}PriorityWarnings'.format(priority.capitalize())])

    def metric_source_urls(self, *job_names):
        """ Return the url of the job. """
        return [self.__report_url.format(job=self.resolve_job_name(job_name)) for job_name in job_names]
