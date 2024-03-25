import json
import random
import string


class RequestUtils:

    @staticmethod
    def get_random_string(length):
        """
        Method to build a random string
        :length:   int   Number to define the length of the string
        :return:         The random string
        """
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def space_body(self, name, multi_assign=True):
        """
        Method to build the body for space request.
        :namer:   Str     Name of space
        :return:          Body for space request in JSON.
        """
        name_complement = self.get_random_string(4)
        body_space = {
            "name": f"Space-{name}-{name_complement}",
            "multiple_assignees": multi_assign,
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
        return json.dumps(body_space)

    @staticmethod
    def build_post_headers(token):
        """
        Method to build headers of post request
        :param token:     Str   Token
        :return:
        """
        headers = {
            "Authorization": f"{token}",
            "Content-Type": "application/json"
        }
        return headers

    def build_folder_body(self, name):
        """
        Method to build the body for space request.
        :namer:   Str     Name of space
        :return:          Body for space request in JSON.
        """
        name_complement = self.get_random_string(4)
        body_folder = {
            "name": f"folder-{name}-{name_complement}"
        }
        return json.dumps(body_folder)
