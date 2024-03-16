import json
import logging

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestTeamSpace:

    @classmethod
    def setup_class(cls):
        LOGGER.debug("Setup Class method")
        cls.list_space = []
        cls.rest_client = RestClient()
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
            if response.status_code == 200:
                LOGGER.info("Space Id: %s deleted", id_space)

    def __get_team_id(self):
        rest_client = self.rest_client
        response = rest_client.request("get", URL_CLICKUP+"/team")
        team_id = response.json()["teams"][0]["id"]
        LOGGER.debug("Team ID: %s", team_id)
        return team_id

    def test_create_space(self):
        """
        Test create space
        """
        body_space = {
                "name": "MP-API courseSpace01",
                "multiple_assignees": True,
                "features": {
                    "due_dates": {
                        "enabled": True,
                        "start_date": False,
                        "remap_due_dates": True,
                        "remap_closed_due_date": False
                    },
                    "time_tracking": {
                        "enabled": False
                    },
                    "tags": {
                        "enabled": True
                    },
                    "time_estimates": {
                        "enabled": True
                    },
                    "checklists": {
                        "enabled": True
                    },
                    "custom_fields": {
                        "enabled": True
                    },
                    "remap_dependencies": {
                        "enabled": True
                    },
                    "dependency_warning": {
                        "enabled": True
                    },
                    "portfolios": {
                        "enabled": True
                    }
                }
            }
        body = json.dumps(body_space)
        headers_post = {
            "Authorization": f"{CLICKUP_TOKEN}",
            "Content-Type": "application/json"
        }
        rest_client = RestClient(headers=headers_post)
        response = rest_client.request("post", url=self.url_team_space, body=body)
        self.id_space_created = response.json()["id"]
        self.list_space.append(self.id_space_created)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_get_all_spaces(self):
        rest_client = self.rest_client
        url_get_space = f"{self.url_team_space}?archived=false"
        response = rest_client.request("get", url=url_get_space)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_get_a_space(self, create_space, test_log_name):
        rest_client = self.rest_client
        url_get_space = f"{self.url_space}/{create_space}"
        response = rest_client.request("get", url=url_get_space)
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_update_a_space(self, create_space, test_log_name):

        name_space_to_update = "MP-API courseSpace01 - Updated"
        body_space_updated = {
            "name": name_space_to_update,
            "multiple_assignees": True,
            "features": {
                "due_dates": {
                    "enabled": True,
                    "start_date": False,
                    "remap_due_dates": True,
                    "remap_closed_due_date": False
                },
                "time_tracking": {
                    "enabled": False
                },
                "tags": {
                    "enabled": True
                },
                "time_estimates": {
                    "enabled": True
                },
                "checklists": {
                    "enabled": True
                },
                "custom_fields": {
                    "enabled": True
                },
                "remap_dependencies": {
                    "enabled": True
                },
                "dependency_warning": {
                    "enabled": True
                },
                "portfolios": {
                    "enabled": True
                }
            }
        }
        body = json.dumps(body_space_updated)
        url_put = {
            "Authorization": f"{CLICKUP_TOKEN}",
            "Content-Type": "application/json"
        }
        rest_client = RestClient(headers=url_put)
        url_get_space = f"{self.url_space}/{create_space}"
        response = rest_client.request("put", url=url_get_space, body=body)
        space_name_updated = response.json()["name"]
        assert space_name_updated == name_space_to_update, (f"Name is not updated expected name {name_space_to_update}"
                                                            f"current {space_name_updated}")
        assert response.status_code == 200, "wrong status code, expected 200"

    def test_delete_space(self, create_space, test_log_name):
        rest_client = self.rest_client
        url_get_space = f"{self.url_space}/{create_space}"
        response = rest_client.request("delete", url=url_get_space)
        assert response.status_code == 200, "wrong status code, expected 200"

