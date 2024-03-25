import json
import logging

import pytest
import requests

from config.config import URL_CLICKUP, CLICKUP_TOKEN
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_space(request, get_team_id):
    LOGGER.debug("Create Space fixture")
    environment = request.config.getoption("--env")
    LOGGER.critical("Environment selected: %s", environment)
    body_space = {
        "name": "MP-API courseSpace - 04",
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
    response = rest_client.request("post", URL_CLICKUP+"/team/"+get_team_id+"/space", body=body)
    id_space = response["body"]["id"]
    yield id_space
    delete_space(id_space, rest_client)


@pytest.fixture()
def create_folder(create_space):

    LOGGER.debug("Create folder fixture")
    body_folder = {
        "name": "folder-name"
    }
    body = json.dumps(body_folder)
    headers_post = {
        "Authorization": f"{CLICKUP_TOKEN}",
        "Content-Type": "application/json"
    }
    url_folder = f"{URL_CLICKUP}/space/{create_space}/folder"
    rest_client = RestClient(headers=headers_post)
    response = rest_client.request("post", url_folder, body=body)
    id_folder_created = response["body"]["id"]
    yield id_folder_created


@pytest.fixture()
def get_team_id():

    rest_client = RestClient()
    response = rest_client.request("get", URL_CLICKUP+"/team")
    team_id = response["body"]["teams"][0]["id"]
    LOGGER.debug("Team ID: %s", team_id)
    return team_id


def delete_space(id_space, rest_client):
    LOGGER.info("Cleanup space...")
    url_delete_project = f"{URL_CLICKUP}/space/{id_space}"
    response = rest_client.request("delete", url=url_delete_project)
    if response["status_code"] == 200:
        LOGGER.info("Project Id: %s deleted", id_space)


@pytest.fixture()
def test_log_name(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )