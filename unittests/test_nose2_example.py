import logging
import unittest

from nose2.tools import params

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestNose2Example(unittest.TestCase):

    def setUp(self):
        LOGGER.debug("Setup")

    @classmethod
    def setUpClass(cls):
        LOGGER.debug("Setup class")

    def tearDown(self):
        LOGGER.debug("Teardwon")

    @classmethod
    def tearDownClass(cls):
        LOGGER.debug("Teardown classs")

    def test_example_one(self):
        LOGGER.debug("test one")

    def test_example_dos(self):
        LOGGER.debug("test dos")

    @params("name1", "name2")
    def test_example_3(self, name):
        LOGGER.debug(name)


if __name__ == '__main__':
    unittest.main()
