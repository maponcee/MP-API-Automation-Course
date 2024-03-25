import logging

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from helpers.validate_response import ValidateResponse
from utils.logger import get_logger
from utils.request_utils import RequestUtils

LOGGER = get_logger(__name__, logging.DEBUG)


class TestTeamSpace:

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
        team_id = cls.__get_team_id(cls)
        cls.url_team_space = f"{URL_CLICKUP}/team/{team_id}/space"
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

    def __get_team_id(self):
        response = self.rest_client.request("get", URL_CLICKUP+"/team")
        team_id = response["body"]["teams"][0]["id"]
        LOGGER.debug("Team ID: %s", team_id)
        return team_id

    def test_create_space(self, test_log_name):
        """
        Test create space
        :param test_log_name:
        """
        body_space = self.request_utils.space_body("post_request")
        headers_post = self.request_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("post", url=self.url_team_space, body=body_space)
        self.id_space_created = response["body"]["id"]
        self.list_space.append(self.id_space_created)
        self.validate.validate_response(response, "create_space")

    def test_get_all_spaces(self, test_log_name):
        """
        Test case to get all spaces created
        :param test_log_name:
        """
        rest_client = self.rest_client
        url_get_space = f"{self.url_team_space}?archived=false"
        response = rest_client.request("get", url=url_get_space)
        self.validate.validate_response(response, "get_all_spaces")

    def test_get_a_space(self, create_space, test_log_name):
        """
        Test to get a created space
        :param create_space:  str     ID of created space
        :param test_log_name:
        """
        rest_client = self.rest_client
        url_get_space = f"{self.url_space}/{create_space}"
        response = rest_client.request("get", url=url_get_space)
        self.validate.validate_response(response, "get_a_space")

    def test_update_a_space(self, create_space, test_log_name):
        """
        Test cases to validate that it is possible to update the space information.
        :param create_space:  Str    The UD os the space created
        :param test_log_name:
        """
        body_space_updated = self.request_utils.space_body("Updated")
        url_put = self.request_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=url_put)
        url_get_space = f"{self.url_space}/{create_space}"
        response = rest_client.request("put", url=url_get_space, body=body_space_updated)
        self.validate.validate_response(response, "update_a_space")

    def test_delete_space(self, create_space, test_log_name):
        """
        Test to delete a created space
        :param create_space:  Str    The UD os the space created
        :param test_log_name:
        """
        rest_client = self.rest_client
        url_get_space = f"{self.url_space}/{create_space}"
        response = rest_client.request("delete", url=url_get_space)
        self.validate.validate_response(response, "delete_a_space")
