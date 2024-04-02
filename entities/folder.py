"""
(c) Copyright Jalasoft. 2024

folder.py
    Entity class for folder feature.
"""
import json
import logging

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from utils.logger import get_logger
from utils.request_utils import RequestUtils

LOGGER = get_logger(__name__, logging.DEBUG)


class Folder:
    """
    Entity class for folders
    """

    def __init__(self, rest_client=None):
        self.url_folders = f"{URL_CLICKUP}/folder"
        if rest_client is None:
            self.rest_client = RestClient()
        self.rest_utils = RequestUtils()

    def create_folder(self, space_id):
        """
        Method to create a folder in the space
        :param space_id:     STR     ID of space to create the folder
        :return:
        """
        randon_string = self.rest_utils.get_random_string(3)
        body_folder = {
            "name": f"folder-name-{randon_string}"
        }
        body = json.dumps(body_folder)
        url_folder = f"{URL_CLICKUP}/space/{space_id}/folder"
        headers_post = self.rest_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("post", url=url_folder, body=body)
        return response, self.rest_client

    def delete_folder(self, folder_id):
        """
        Delete folder
        :param folder_id:   STR    Folder id to delete.
        """
        LOGGER.info("Cleanup space...")
        url_delete_folder = f"{self.url_folders}/{folder_id}"
        response = self.rest_client.request("delete", url=url_delete_folder)
        if response["status_code"] == 200:
            LOGGER.info("Folder Id: %s deleted", folder_id)
