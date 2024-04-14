"""
(c) Copyright Jalasoft. 2024

test_teamspace.py
    File  to test the space feature
"""
import logging

import allure
import pytest

from config.config import URL_CLICKUP, CLICKUP_TOKEN, MAX_SPACES
from entities.space import Space
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger
from utils.request_utils import RequestUtils

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("API task")
@allure.story("Team Space")
class TestTeamSpace:
    """
    Class to test the space feature.
    """

    @classmethod
    def setup_class(cls):
        """
        Class method to initialize the class
        """
        LOGGER.debug("Setup Class method")
        cls.list_space = []
        cls.rest_client = RestClient()
        cls.request_utils = RequestUtils()
        cls.validate = ValidateResponse()
        cls.url_space = f"{URL_CLICKUP}/space"

    def teardown_class(self):
        """
        Delete all cards used in test
        """
        LOGGER.info("Cleanup spaces...")
        for id_space in self.list_space:
            url_delete_space = f"{self.url_space}/{id_space}"
            response = self.rest_client.request("delete", url=url_delete_space)
            if response["status_code"] == 200:
                LOGGER.info("Space Id: %s deleted", id_space)

    @allure.title("Test create a space")
    @allure.tag("acceptance", "space")
    @pytest.mark.acceptance
    def test_create_space(self, _get_team_id, _test_log_name):
        """
        Test create space
        :param test_log_name:
        """
        space = Space()
        url_get_space = f"{URL_CLICKUP}/team/{_get_team_id}/space?archived=false"
        response, _ = space.create_space(url_space=url_get_space, name_space="create_test")
        id_space_created = response["body"]["id"]
        self.list_space.append(id_space_created)
        self.validate.validate_response(response, "create_space")

    @allure.title("Test get all spaces from a team")
    @allure.tag("acceptance", "space")
    @pytest.mark.acceptance
    def test_get_all_spaces(self, _get_team_id, _test_log_name):
        """
        Test case to get all spaces created
        :param test_log_name:
        """
        url_get_space = f"{URL_CLICKUP}/team/{_get_team_id}/space?archived=false"
        response = self.rest_client.request("get", url=url_get_space)
        self.validate.validate_response(response, "get_all_spaces")

    @allure.title("Test get a space")
    @allure.tag("acceptance", "space")
    @pytest.mark.acceptance
    def test_get_a_space(self, _create_space, _test_log_name):
        """
        Test to get a created space
        :param create_space:  str     ID of created space
        :param test_log_name:
        """
        rest_client = self.rest_client
        url_get_space = f"{self.url_space}/{_create_space}"
        response = rest_client.request("get", url=url_get_space)
        self.validate.validate_response(response, "get_a_space")

    @allure.title("Test update a space")
    @allure.tag("acceptance", "space")
    @pytest.mark.acceptance
    def test_update_a_space(self, _create_space, _test_log_name):
        """
        Test cases to validate that it is possible to update the space information.
        :param create_space:  Str    The UD os the space created
        :param test_log_name:
        """
        body_space_updated = self.request_utils.build_space_body("Updated")
        url_put = self.request_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=url_put)
        url_get_space = f"{self.url_space}/{_create_space}"
        response = rest_client.request("put", url=url_get_space, body=body_space_updated)
        self.validate.validate_response(response, "update_a_space")

    @allure.title("Test delete a space")
    @allure.tag("acceptance", "space")
    @pytest.mark.acceptance
    def test_delete_space(self, _create_space, _test_log_name):
        """
        Test to delete a created space
        :param create_space:  Str    The UD os the space created
        :param test_log_name:
        """
        rest_client = self.rest_client
        url_get_space = f"{self.url_space}/{_create_space}"
        response = rest_client.request("delete", url=url_get_space)
        self.validate.validate_response(response, "delete_a_space")

    @allure.title("Test the maximum number of spaces that can be created")
    @allure.tag("functional", "space")
    @pytest.mark.functional
    def test_max_number_of_space(self, _get_team_id, _test_log_name):
        """
        Test the max number of spaces allowed
        :param get_team_id:      Str     ID of the team to create the spaces.
        :param test_log_name:
        """

        url_get_space = f"{URL_CLICKUP}/team/{_get_team_id}/space?archived=false"
        spaces = self.rest_client.request("get", url=url_get_space)
        num_spaces = len(spaces["body"]["spaces"])
        LOGGER.debug("Number of current Spaces: %s", num_spaces)
        space = Space()
        for _ in range(num_spaces, MAX_SPACES):
            response, _ = space.create_space(url_space=url_get_space, name_space="max_num_spaces")
            id_space_created = response["body"]["id"]
            self.list_space.append(id_space_created)

        response, _ = space.create_space(url_space=url_get_space, name_space="max_num_spaces")
        assert response["status_code"] == 403
