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

from ... import metric_source
from ...domain import LowerIsBetterMetric


class ZAPScanAlertsMetric(LowerIsBetterMetric):
    """ Base class for metrics that measure the number of ZAP Scan alerts with a certain risk level. """

    unit = 'security waarschuwingen'
    risk_level = risk_level_key = 'Subclass responsilbility'
    norm_template = 'Het product heeft geen {risk_level} risico ZAP Scan {unit}. ' \
                    'Meer dan {low_target} is rood.'
    template = '{name} heeft {value} {risk_level} risico {unit}.'
    target_value = 0
    metric_source_classes = (metric_source.ZAPScanReport,)

    @classmethod
    def norm_template_default_values(cls):
        values = super(ZAPScanAlertsMetric, cls).norm_template_default_values()
        values['risk_level'] = cls.risk_level
        return values

    def value(self):
        return -1 if self._missing() else self.__nr_alerts()

    def _missing(self):
        return self.__nr_alerts() < 0

    def __nr_alerts(self):
        """ Return the number of alerts. """
        return self._metric_source.alerts(self.risk_level_key, *self._metric_source_urls())

    def _parameters(self):
        parameters = super(ZAPScanAlertsMetric, self)._parameters()
        parameters['risk_level'] = self.risk_level
        return parameters


class HighRiskZAPScanAlertsMetric(ZAPScanAlertsMetric):
    """ Metric for measuring the number of high risk ZAP Scan alerts. """

    name = 'Hoeveelheid ZAP Scan waarschuwingen met hoog risiconiveau'
    risk_level = 'hoog'
    risk_level_key = 'high'
    low_target_value = 3


class MediumRiskZAPScanAlertsMetric(ZAPScanAlertsMetric):
    """ Metric for measuring the number of medium risk ZAP Scan alerts. """

    name = 'Hoeveelheid ZAP Scan waarschuwingen met medium risiconiveau'
    risk_level = 'medium'
    risk_level_key = 'medium'
    low_target_value = 10
