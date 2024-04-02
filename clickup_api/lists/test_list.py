"""
(c) Copyright Jalasoft. 2024

test_list.py
    Class to test the list feature
"""
import logging

import allure
import pytest

from config.config import URL_CLICKUP
from entities.list import List
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("API task")
@allure.story("List")
class TestLists:
    """
    Class to test the CRUD of list feature
    """

    @classmethod
    def setup_class(cls):
        """
        Class method to initialize the class
        """
        LOGGER.debug("Setup Class method")
        cls.list_of_lists = []
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.list = List()
        cls.url_list = f"{URL_CLICKUP}/list/"

    @allure.title("Test create a list for space")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_create_list_for_space(self, create_space, test_log_name):
        """
        Test to create a list in a space
        :param create_space:   Str    ID of created space
        :param test_log_name:
        """
        response, _ = self.list.create_list(space_id=create_space)
        id_list = response["body"]["id"]
        self.list_of_lists.append(id_list)
        self.validate.validate_response(response, "create_list")

    @allure.title("Test create a list for folder")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_create_list_for_folder(self, create_folder, test_log_name):
        """
        Test create a list for a folder
        :param create_folder:    Str   ID of created folder
        :param test_log_name:
        """
        response, _ = self.list.create_list(folder_id=create_folder)
        id_list = response["body"]["id"]
        self.list_of_lists.append(id_list)
        self.validate.validate_response(response, "create_list")

    @allure.title("Test get all lists of space")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_get_all_folder_lists(self, create_list_of_folder):
        """
        Test to retrieve all lists created in a folder
        :param create_list_of_folder:   tuple    Ids of list and folder
        """
        _, folder_id = create_list_of_folder
        url_folder = f"{URL_CLICKUP}/folder/{folder_id}/list?archived=false"
        response = self.rest_client.request("get", url=url_folder)
        self.validate.validate_response(response, "get_all_list")

    @allure.title("Test get all lists of folder")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_get_all_space_lists(self, create_list_of_space):
        """
        Test to retrieve all lists created in a space
        :param create_list_of_space:   tuple    Ids of list and space
        """
        _, space_id = create_list_of_space
        url_space = f"{URL_CLICKUP}/space/{space_id}/list?archived=false"
        response = self.rest_client.request("get", url=url_space)
        self.validate.validate_response(response, "get_all_list")

    @allure.title("Test get a lists")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_get_a_list(self, create_list_of_space):
        """
        Test to retrieve a list
        :param create_list_of_space:   tuple    Ids of list and space
        """
        list_id, _ = create_list_of_space
        url_list = f"{self.url_list}/{list_id}"
        response = self.rest_client.request("get", url=url_list)
        self.validate.validate_response(response, "get_a_list")

    @allure.title("Test update a lists")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_update_a_list(self, create_list_of_space):
        """
        Test to update a list
        :param create_list_of_space:   tuple    Ids of list and space
        """
        list_id, _ = create_list_of_space
        response, _ = self.list.update_list(list_id=list_id)
        self.validate.validate_response(response, "get_a_list")

    @allure.title("Test delete a lists")
    @allure.tag("acceptance", "lists")
    @pytest.mark.acceptance
    def test_delete_a_list(self, create_list_of_folder):
        """
        Test to delete a list
        :param create_list_of_folder:   tuple    Ids of list and space
        """
        list_id, _ = create_list_of_folder
        url_list = f"{self.url_list}/{list_id}"
        response = self.rest_client.request("delete", url=url_list)
        self.validate.validate_response(response, "delete_a_list")

    @allure.title("Test the create using allowed priorities")
    @allure.tag("functional", "lists")
    @pytest.mark.functional
    def test_allowed_priorities_for_list(self, create_space, test_log_name):
        """
        Test to verify it is possible to create a list with all allowed priorities
        :param create_space:      Str     ID of the team to create the spaces.
        :param test_log_name:
        """
        for index in range(1, 5):
            response, _ = self.list.create_list(space_id=create_space, priority=index)
            id_list = response["body"]["id"]
            self.list_of_lists.append(id_list)
            self.validate.validate_response(response, "create_list")
