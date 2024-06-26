"""
(c) Copyright Jalasoft. 2024

validate_response.py
    Validate class for validate the response of the request
"""
import json
import logging

from config.config import abs_path
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class ValidateResponse:
    """
    Class to build the method to validate the responses of request.
    """

    def validate_response(self, actual_response=None, endpoint=None):
        """
        Method to get the file to compare with the actual response
        :param actual_response:
        :param endpoint:
        """

        expected_response = self.read_input_data_json(
            f"{abs_path}/clickup_api/input_data/{endpoint}.json")

        if "body" in actual_response:
            self.validate_value(expected_response["status_code"], actual_response["status_code"],
                                "status_code")
            self.validate_value(expected_response["response"]["body"], actual_response["body"],
                                "body")
            self.validate_value(expected_response["headers"],  actual_response["headers"],
                                "headers")

    def validate_value(self, expected_value, actual_value, key_compare):
        """
        Method to compare 2 values, according the key_compare
        :param expected_value:
        :param actual_value:
        :param key_compare:
        """
        LOGGER.info("Validating %s: ", key_compare)
        error_message = f"Expecting '{expected_value}' but received '{actual_value}'"
        if key_compare == "body":
            if isinstance(actual_value, list):
                assert self.compare_json(expected_value[0], actual_value[0]), error_message
            else:
                assert self.compare_json(expected_value, actual_value), error_message
        elif key_compare == "headers":
            LOGGER.debug("Expected Headers: %s", expected_value.items())
            LOGGER.debug("Actual Headers: %s", actual_value.items())
            assert expected_value.items() <= actual_value.items(), error_message
        else:
            LOGGER.debug("Expected Status Code: %s", expected_value)
            LOGGER.debug("Actual Status Code: %s", actual_value)
            assert expected_value == actual_value, error_message

    @staticmethod
    def read_input_data_json(file_name):
        """
        Method to reed a file information.
        :param file_name:
        :return:
        """
        LOGGER.debug("Reading file '%s'", file_name)
        with open(file_name, encoding="utf8") as json_file:
            data = json.load(json_file)
        LOGGER.debug("Content of '%s': '%s'", file_name, data)
        json_file.close()

        return data

    @staticmethod
    def compare_json(json1, json2):
        """
        Method to compare the 2 jsons
        :param json1:
        :param json2:
        :return:
        """
        for key in json1.keys():
            if key in json2.keys():
                LOGGER.debug("Key '%s' found in json2", key)
            else:
                LOGGER.debug("Key '%s' not found in json2", key)
                return False
        return True
