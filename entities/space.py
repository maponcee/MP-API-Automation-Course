import logging

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from utils.logger import get_logger
from utils.request_utils import RequestUtils

LOGGER = get_logger(__name__, logging.DEBUG)


class Space:

    def __init__(self, rest_client=None):
        self.url_spaces = f"{URL_CLICKUP}/space"
        if rest_client is None:
            self.rest_client = RestClient()
        self.rest_utils = RequestUtils()

    def create_space(self, url_space, name_space=None):
        """
        Method to create a space in the team
        :param url_space:     STR     Endpoint to execute the create request
        :param name_space:    STR     The name to create a space.
        :return:
        """
        if name_space is None:
            body_space = self.rest_utils.build_space_body(name="entity")
        else:
            body_space = self.rest_utils.build_space_body(name=name_space)
        headers_post = self.rest_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("post", url=url_space, body=body_space)
        return response, self.rest_client

    def delete_space(self, space_id):
        """
        Delete Space
        :param space_id:   STR     ID of the created space
        """
        LOGGER.info("Cleanup space...")
        url_delete_space = f"{self.url_spaces}/{space_id}"
        response = self.rest_client.request("delete", url=url_delete_space)
        if response["status_code"] == 200:
            LOGGER.info("Space Id: %s deleted", space_id)
