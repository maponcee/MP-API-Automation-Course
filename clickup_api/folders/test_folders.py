import logging

import allure
import pytest

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger
from utils.request_utils import RequestUtils

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("API task")
@allure.story("Folders")
class TestFolders:
    """
    Class to test the CRUD of folders feature
    """

    @classmethod
    def setup_class(cls):
        """
        Class method to initialize the class
        """
        LOGGER.debug("Setup Class method")
        cls.list_folders = []
        cls.rest_client = RestClient()
        cls.request_utils = RequestUtils()
        cls.validate = ValidateResponse()
        cls.url_space = f"{URL_CLICKUP}/space/"
        cls.url_folder = f"{URL_CLICKUP}/folder/"

    @allure.title("Test create a folder")
    @allure.tag("acceptance", "folder")
    @pytest.mark.acceptance
    def test_create_folder(self, create_space, test_log_name):
        """
        Test to create a folder in a space
        :param create_space:   Str    ID of created space
        :param test_log_name:
        """
        url_folder = f"{self.url_space}{create_space}/folder"
        headers_post = self.request_utils.build_post_headers(CLICKUP_TOKEN)
        body_folder = self.request_utils.build_folder_body("create")
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("post", url=url_folder, body=body_folder)
        id_folder = response["body"]["id"]
        self.list_folders.append(id_folder)
        self.validate.validate_response(response, "create_folder")

    @allure.title("Test get all folders from a space")
    @allure.tag("acceptance", "folder")
    @pytest.mark.acceptance
    def test_get_all_folders(self, create_space, test_log_name):
        """
        Test case to get all folders created
        :param test_log_name:
        """
        url_folder = f"{self.url_space}{create_space}/folder"
        headers_post = self.request_utils.build_post_headers(CLICKUP_TOKEN)
        body_folder = self.request_utils.build_folder_body("create")
        rest_client = RestClient(headers=headers_post)
        response_create_folder = rest_client.request("post", url=url_folder, body=body_folder)
        id_folder = response_create_folder["body"]["id"]
        self.list_folders.append(id_folder)
        response = self.rest_client.request("get", url=url_folder)
        self.validate.validate_response(response, "get_all_folders")

    @allure.title("Test get a folder")
    @allure.tag("acceptance", "folder")
    @pytest.mark.acceptance
    def test_get_a_folder(self, create_folder, test_log_name):
        """
        Test to get a created folder
        :param create_folder:  str     ID of created folder
        :param test_log_name:
        """
        url_get_folder = f"{self.url_folder}/{create_folder}"
        response = self.rest_client.request("get", url=url_get_folder)
        self.validate.validate_response(response, "create_folder")

    @allure.title("Test update a folder")
    @allure.tag("acceptance", "folder")
    @pytest.mark.acceptance
    def test_update_a_folder(self, create_folder, test_log_name):
        """
        Test cases to validate that it is possible to update the folder information.
        :param create_folder:  Str    The ID of the created folder
        :param test_log_name:
        """
        body_folder_updated = self.request_utils.build_space_body("Updated")
        url_put = self.request_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=url_put)
        url_get_folder = f"{self.url_folder}/{create_folder}"
        response = rest_client.request("put", url=url_get_folder, body=body_folder_updated)
        self.validate.validate_response(response, "create_folder")

    @allure.title("Test delete a folder")
    @allure.tag("acceptance", "folder")
    @pytest.mark.acceptance
    def test_delete_folder(self, create_folder, test_log_name):
        """
        Test to delete a created folder
        :param create_folder:  Str    The UD os the folder created
        :param test_log_name:
        """
        rest_client = self.rest_client
        url_get_folder = f"{self.url_folder}/{create_folder}"
        response = rest_client.request("delete", url=url_get_folder)
        self.validate.validate_response(response, "delete_a_folder")
