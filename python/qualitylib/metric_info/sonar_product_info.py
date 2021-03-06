"""pyright 2012-2016 Ministerie van Sociale Zaken en Werkgelegenheid

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


class SonarProductInfo(object):
    """ Class to represent information that Sonar has about a product. """
    def __init__(self, sonar, product):
        self.__sonar = sonar
        self.__product = product

    def sonar_id(self):
        """ Return the id that identifies the product in Sonar. """
        if not self.__product:
            return ''
        return self.__product.metric_source_id(self.__sonar) or ''

    def all_sonar_ids(self):
        """ Return all Sonar ids of the product: the Sonar id of the product itself and its unit tests
            if applicable. """
        sonar_ids = set()
        for component in [self.__product, self.__product.unittests(), self.__product.jsf()]:
            if component:
                component_sonar_info = SonarProductInfo(self.__sonar, component)
                if component_sonar_info.sonar_id():
                    sonar_ids.add(component_sonar_info.sonar_id())
        return sonar_ids

    def latest_version(self):
        """ Return the latest version of the product. """
        if self.sonar_id():
            # Product is a branch or trunk version, get the SNAPSHOT version number from Sonar
            return self.__sonar.version(self.sonar_id())
        else:
            return ''
