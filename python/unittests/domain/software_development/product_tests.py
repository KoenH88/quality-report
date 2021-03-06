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

import unittest

from qualitylib import domain, requirement


class ProductTest(unittest.TestCase):
    """ Unit tests for the Product domain class. """
    def setUp(self):
        self.__project = domain.Project('Organization')
        self.__product = domain.Product(self.__project, name='Product')

    def test_product_name(self):
        """ Test that the name of the product equals given name. """
        self.assertEqual('Product', self.__product.name())

    def test_default_unittests(self):
        """ Test that products have no unit test component by default. """
        self.assertFalse(self.__product.unittests())

    def test_unittests(self):
        """ Test that the unit test component can be retrieved. """
        unittests = domain.Product(self.__project)
        product = domain.Product(self.__project, unittests=unittests)
        self.assertEqual(unittests, product.unittests())

    def test_default_integration_tests(self):
        """ Test that products have no integration test component by default. """
        self.assertFalse(self.__product.integration_tests())

    def test_integration_tests(self):
        """ Test that the integration test component can be retrieved. """
        integration_tests = domain.Product(self.__project)
        product = domain.Product(self.__project, integration_tests=integration_tests)
        self.assertEqual(integration_tests, product.integration_tests())

    def test_default_jsf(self):
        """ Test that products have no jsf component by default. """
        self.assertFalse(self.__product.jsf())

    def test_jsf(self):
        """ Test that the jsf component can be retrieved. """
        jsf = domain.Product(self.__project)
        self.assertEqual(jsf, domain.Product(self.__project, jsf=jsf).jsf())

    def test_default_art(self):
        """ Test that products have no automated regression test by default. """
        self.assertFalse(self.__product.art())

    def test_art(self):
        """ Test that the automated regression test can be retrieved. """
        art = domain.Product(self.__project)
        self.assertEqual(art, domain.Product(self.__project, art=art).art())

    def test_is_main(self):
        """ Test that the product is part of the main system by default. """
        self.assertTrue(self.__product.is_main())


class ComponentTest(unittest.TestCase):
    """ Unit test for the component class. """
    def test_default_requirements(self):
        """ Test that the default requirements are correct. """
        self.assertEqual({requirement.CodeQuality, requirement.UnitTests, requirement.TrackBranches},
                         domain.Component.default_requirements())

    def test_optional_requirements(self):
        """ Test that the optional requirements don't contain the default requirements. """
        self.failIf(domain.Component.default_requirements() & domain.Component.optional_requirements())


class ApplicationTest(unittest.TestCase):
    """ Unit test for the application class. """
    def test_default_rquirements(self):
        """ Test that the default requirements are correct. """
        self.assertEqual({requirement.CodeQuality, requirement.TrackBranches, requirement.Performance,
                          requirement.ART, requirement.ARTCoverage, requirement.OWASPZAP, requirement.OWASPDependencies,
                          requirement.OpenVAS},
                         domain.Application.default_requirements())

    def test_optional_requirements(self):
        """ Test that the optional requirements don't contain the default requirements. """
        self.failIf(domain.Application.default_requirements() & domain.Application.optional_requirements())

