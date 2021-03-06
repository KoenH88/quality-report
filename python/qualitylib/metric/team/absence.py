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


class TeamAbsence(LowerIsBetterMetric):
    """ Metric for measuring the number of consecutive days that multiple team members are absent. """

    name = 'Absentie'
    unit = 'werkdagen'
    norm_template = 'Het aantal aaneengesloten {unit} dat meerdere teamleden tegelijk gepland afwezig zijn is ' \
        'lager dan {target} {unit}. Meer dan {low_target} {unit} is rood. Het team bestaat uit {team}.'
    template = 'De langste periode dat meerdere teamleden tegelijk gepland afwezig zijn is {value} {unit} ' \
        '({start} tot en met {end}). Afwezig zijn: {absentees}.'
    perfect_template = 'Er zijn geen teamleden tegelijk gepland afwezig.'
    target_value = 5
    low_target_value = 10
    metric_source_classes = (metric_source.HolidayPlanner,)

    @classmethod
    def is_applicable(cls, team):
        return len(team.members()) > 1

    @classmethod
    def norm_template_default_values(cls):
        values = super(TeamAbsence, cls).norm_template_default_values()
        values['team'] = '(Lijst van teamleden)'
        return values

    def value(self):
        return self._metric_source.days(self._subject)[0] if self._metric_source else -1

    def _parameters(self):
        # pylint: disable=protected-access
        parameters = super(TeamAbsence, self)._parameters()
        parameters['team'] = ', '.join([member.name() for member in self._subject.members()])
        if self._metric_source:
            length, start, end, members = self._metric_source.days(self._subject)
            if length:
                parameters['start'] = start.isoformat()
                parameters['end'] = end.isoformat()
                parameters['absentees'] = ', '.join(sorted([member.name() for member in members]))
        return parameters
