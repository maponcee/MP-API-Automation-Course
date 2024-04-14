"""
(c) Copyright Jalasoft. 2024

list.py
    Entity class for list feature.
"""
import json
import logging

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from utils.logger import get_logger
from utils.request_utils import RequestUtils

LOGGER = get_logger(__name__, logging.DEBUG)


class List:
    """
    Entities class for List features.
    """

    def __init__(self, rest_client=None):
        self.url_list = f"{URL_CLICKUP}/list"
        if rest_client is None:
            self.rest_client = RestClient()
        self.rest_utils = RequestUtils()

    def create_list(self, folder_id=None, space_id=None, priority=1):
        """
        Create a list.
        :param folder_id:   Str    ID of folder to create the list
        :param space_id:    Str    ID of space to create the list
        :param priority:    Int    Priority of list
        :return:
        """
        url_list = ""
        randon_string = self.rest_utils.get_random_string(3)
        body_list = {
            "name": f"API List -{randon_string}",
            "content": "New List Content",
            "due_date_time": False,
            "priority": priority,
            "status": "red"
        }
        body = json.dumps(body_list)
        if folder_id:
            url_list = f"{URL_CLICKUP}/folder/{folder_id}/list"
        if space_id:
            url_list = f"{URL_CLICKUP}/space/{space_id}/list"
        headers_post = self.rest_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("post", url=url_list, body=body)
        return response, self.rest_client

    def delete_list(self, list_id):
        """
        Delete list
        :param list_id:   Str   List Id to delete
        """
        LOGGER.info("Clean list...")
        url_delete_list = f"{self.url_list}/{list_id}"
        response = self.rest_client.request("delete", url=url_delete_list)
        if response["status_code"] == 200:
            LOGGER.info("List ID: %s deleted", list_id)

    def update_list(self, list_id):
        """
        Update a list.
        :param list_id:   Str    ID of list to update
        :return:
        """
        randon_string = self.rest_utils.get_random_string(3)
        body_list = {
            "name": f"API List- Updated-{randon_string}",
            "content": "New List Content",
            "due_date_time": False,
            "priority": 1,
            "status": "red",
            "unset_status": True
        }
        body = json.dumps(body_list)
        url_list = f"{self.url_list}/{list_id}"
        headers_post = self.rest_utils.build_post_headers(CLICKUP_TOKEN)
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("put", url=url_list, body=body)
        return response, self.rest_client
