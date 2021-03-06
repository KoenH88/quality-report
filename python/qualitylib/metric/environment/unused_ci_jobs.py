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
from __future__ import absolute_import

from qualitylib.domain import LowerIsBetterMetric
from qualitylib import metric_source


class UnusedCIJobs(LowerIsBetterMetric):
    """ Metric for measuring the number of continuous integration jobs that are not used. """

    name = 'Hoeveelheid ongebruikte CI-jobs'
    unit = 'CI-jobs'
    norm_template = 'Maximaal {target} van de actieve {unit} is ongebruikt. Meer dan {low_target} {unit} is rood. ' \
        'Een CI-job is ongebruikt als er de afgelopen 6 maanden geen bouwpogingen zijn geweest. Inactieve ' \
        '{unit} worden genegeerd.'
    template = '{value} van de {number_of_jobs} actieve {unit} is ongebruikt.'
    url_label_text = 'Ongebruikte jobs'
    target_value = 0
    low_target_value = 2
    metric_source_classes = (metric_source.Jenkins,)

    def _parameters(self):
        # pylint: disable=protected-access
        parameters = super(UnusedCIJobs, self)._parameters()
        parameters['number_of_jobs'] = self.__number_of_jobs()
        return parameters

    def value(self):
        """ Return the number of unused jobs. """
        url = self._metric_source.unused_jobs_url()
        return -1 if url is None else len(url)

    def url(self):
        """ Return the urls for the unused jobs. """
        url = self._metric_source.unused_jobs_url()
        return dict() if url is None else url

    def __number_of_jobs(self):
        """ Return the total number of active jobs. """
        return self._metric_source.number_of_active_jobs()
