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

import datetime
import unittest

from qualitylib import metric, domain, metric_source, requirement


class FakeBoard(object):
    """ Fake a Trello board. """
    metric_source_name = metric_source.TrelloActionsBoard.metric_source_name
    needs_metric_source_id = metric_source.TrelloActionsBoard.needs_metric_source_id

    @staticmethod
    def url():
        """ Return a fake url. """
        return 'http://trello/board'

    @staticmethod
    def date_of_last_update():
        """ Fake the date of the last update. """
        return datetime.datetime.now() - datetime.timedelta(minutes=1)

    @staticmethod
    def over_due_or_inactive_cards_url():
        """ Fake the url. """
        return {'Some card': 'http://trello/some_card', 'Some other card': 'http://trello/other_card'}

    @staticmethod
    def nr_of_over_due_or_inactive_cards():
        """ Fake the number. """
        return 5


class UnreachableBoard(FakeBoard):
    """ Pretend that Trello is down. """

    @staticmethod
    def url():
        """ Return a fake url. """
        return 'http://trello.com'

    @staticmethod
    def date_of_last_update():
        """ Fake that Trello is down. """
        return datetime.datetime.min

    @staticmethod
    def over_due_or_inactive_cards_url():
        """ Fake the url. """
        return {UnreachableBoard.metric_source_name: 'http://trello.com'}

    @staticmethod
    def nr_of_over_due_or_inactive_cards():
        """ Fake that Trello is down. """
        return -1


class RiskLogTest(unittest.TestCase):
    """ Unit tests for the risk log metric. """

    def setUp(self):
        self.__project = domain.Project(
            metric_sources={metric_source.TrelloRiskBoard: FakeBoard()},
            requirements=[requirement.TrackRisks])
        self.__metric = metric.RiskLog(project=self.__project)

    def test_url(self):
        """ Test that the url of the metric uses the url of the risk log board. """
        self.assertEqual({FakeBoard.metric_source_name: FakeBoard().url()}, self.__metric.url())

    def test_value(self):
        """ Test that the value is the number of days since the last update. """
        self.assertEqual(0, self.__metric.value())

    def test_value_without_metric_source(self):
        """ Test that the value is -1 when the metric source hasn't been configured. """
        self.assertEqual(-1, metric.RiskLog(project=domain.Project(requirements=[requirement.TrackRisks])).value())

    def test_should_be_measured(self):
        """ Test that the risk log should be measured if the project has the appropriate requirement. """
        self.assertTrue(metric.RiskLog.should_be_measured(self.__project))


class UnreachableRiskLogTest(unittest.TestCase):
    """ Unit tests for the risk log metric when Trello is unreachable. """

    def setUp(self):
        project = domain.Project(metric_sources={metric_source.TrelloRiskBoard: UnreachableBoard()})
        self.__metric = metric.RiskLog(project=project)

    def test_url(self):
        """ Test that the url of the metric uses the url of the risk log board. """
        self.assertEqual({'Trello acties': 'http://trello.com'}, self.__metric.url())

    def test_value(self):
        """ Test that the value is the number of days since the last update. """
        days = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).days
        self.assertEqual(days, self.__metric.value())


class ActionActivityTest(unittest.TestCase):
    """ Unit tests for the action activity metric. """

    def setUp(self):
        self.__project = domain.Project(metric_sources={metric_source.TrelloActionsBoard: FakeBoard()},
                                        requirements=[requirement.TrackActions])
        self.__metric = metric.ActionActivity(project=self.__project)

    def test_value(self):
        """ Test that the board has been updated today. """
        self.assertEqual(0, self.__metric.value())

    def test_url(self):
        """ Test that url of the metric is equal to the url of the board. """
        self.assertEqual({FakeBoard.metric_source_name: FakeBoard().url()}, self.__metric.url())

    def test_should_be_measured(self):
        """ Test that the metric should be measured when the project has the appropriate requirement. """
        self.assertTrue(metric.ActionActivity.should_be_measured(self.__project))


class UnreachableActionActivityTest(unittest.TestCase):
    """ Unit tests for the action activity metric when Trello is unreachable. """

    def setUp(self):
        project = domain.Project(metric_sources={metric_source.TrelloActionsBoard: UnreachableBoard()},
                                 requirements=[requirement.TrackActions])
        self.__metric = metric.ActionActivity(project=project)

    def test_value(self):
        """ Test that the board has been updated today. """
        days = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).days
        self.assertEqual(days, self.__metric.value())

    def test_url(self):
        """ Test that url of the metric is equal to the url of the board. """
        self.assertEqual({UnreachableBoard.metric_source_name: 'http://trello.com'}, self.__metric.url())


class ActionAgeTest(unittest.TestCase):
    """ Unit tests for the action age metric. """

    def setUp(self):
        self.__project = domain.Project(metric_sources={metric_source.TrelloActionsBoard: FakeBoard()},
                                        requirements=[requirement.TrackActions])
        self.__metric = metric.ActionAge(project=self.__project)

    def test_value(self):
        """ Test that the metric value equals the number of over due or inactive cards. """
        self.assertEqual(FakeBoard().nr_of_over_due_or_inactive_cards(), self.__metric.value())

    def test_url(self):
        """ Test that url of the metric is equal to the url for the over due or inactive cards. """
        self.assertEqual(FakeBoard().over_due_or_inactive_cards_url(), self.__metric.url())

    def test_url_label(self):
        """ Test that the metric has a url label. """
        self.assertTrue(self.__metric.url_label())

    def test_should_be_measured(self):
        """ Test that the metric can be measured when the project has the appropriate requirement. """
        self.assertTrue(metric.ActionAge.should_be_measured(self.__project))


class UnreachableActionAgeTest(unittest.TestCase):
    """ Unit tests for the action age metric when Trello is unreachable. """

    def setUp(self):
        project = domain.Project(metric_sources={metric_source.TrelloActionsBoard: UnreachableBoard()},
                                 requirements=[requirement.TrackActions])
        self.__metric = metric.ActionAge(project=project)

    def test_value(self):
        """ Test that the value indicates a problem. """
        self.assertEqual(-1, self.__metric.value())

    def test_url(self):
        """ Test that url of the metric is equal to the url of the board. """
        self.assertEqual({UnreachableBoard.metric_source_name: 'http://trello.com'}, self.__metric.url())
