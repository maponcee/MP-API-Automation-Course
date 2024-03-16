import logging
import unittest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestUnitTestExample(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()