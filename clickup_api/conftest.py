"""
(c) Copyright Jalasoft. 2024

conftest.py
    File created for pytest fixtures
"""
import logging

import pytest

from config.config import URL_CLICKUP
from entities.folder import Folder
from entities.list import List
from entities.space import Space
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def _create_space(_get_team_id):
    """
    Confid method to create a Space.
    :param _get_team_id:
    :return:
    """
    LOGGER.debug("Team id: %s", _get_team_id)
    LOGGER.debug("Create Space fixture")
    space = Space()
    url_space = f"{URL_CLICKUP}/team/{_get_team_id}/space"
    created_space, _ = space.create_space(url_space, name_space="conf_test")
    id_space = created_space["body"]["id"]
    yield id_space
    delete_space(id_space, space)


@pytest.fixture()
def _create_folder(_create_space):
    """
    Method to create a folder.
    :param _create_space:  STR   ID of space created.
    :return:
    """

    LOGGER.debug("Create folder fixture")
    folder = Folder()
    folder_created, _ = folder.create_folder(_create_space)
    id_folder_created = folder_created["body"]["id"]
    yield id_folder_created
    delete_folder(id_folder_created, folder)


@pytest.fixture()
def create_list_of_folder(_create_folder):
    """
    Method to create a List in a folder
    :param _create_folder:    Str   folder ID to create a list
    :return:
    """
    LOGGER.debug("Folder id: %s", _create_folder)
    obj_list = List()
    list_created, _ = obj_list.create_list(folder_id=_create_folder)
    id_list = list_created["body"]["id"]
    yield id_list, _create_folder
    delete_list(id_list, obj_list)


@pytest.fixture()
def create_list_of_space(_create_space):
    """
    Method to create a List in a space
    :param _create_space:    Str   Space ID to create a list
    :return:
    """
    LOGGER.debug("Space id: %s", _create_space)
    obj_list = List()
    list_created, _ = obj_list.create_list(space_id=_create_space)
    id_list = list_created["body"]["id"]
    yield id_list, _create_space
    delete_list(id_list, obj_list)


@pytest.fixture()
def _get_team_id():
    """
    Method to get the ID of the team
    :return:
    """
    rest_client = RestClient()
    response = rest_client.request("get", URL_CLICKUP+"/team")
    team_id = response["body"]["teams"][0]["id"]
    LOGGER.debug("Team ID: %s", team_id)
    return team_id


def delete_space(id_space, space):
    """
    Method to delete the space.
    :param id_space:   Str   ID of space to delete
    :param space:      Obj   Space object
    """
    space.delete_space(id_space)


def delete_folder(id_folder, folder):
    """
    Method to delete a folder
    :param id_folder:   Str    Folder id to delete
    :param folder:      Obj    Folder object
    """
    folder.delete_folder(id_folder)


def delete_list(id_list, obj_list):
    """
    Method to delete a list.
    :param id_list:    Str    List id to delete
    :param obj_list:   Obj    List object
    """
    obj_list.delete_list(id_list)


@pytest.fixture()
def _test_log_name(request):
    """
    Method for logs
    :param request:
    :return:
    """
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        """
        method to en logs
        """
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)


def pytest_addoption(parser):
    """
    Method to parse the environment
    :param parser:
    """
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )
