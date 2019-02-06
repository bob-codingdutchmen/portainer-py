import json
from urllib.parse import urljoin

import requests


class Portainer:
    FROM_VERSION = (0, 0)

    def __init__(self, host: str):
        self.token = None
        self.host = host

    def login(self, username: str, password: str):
        data = {"Username": username, "Password": password}
        r = self.request("api/auth", method="POST", data=data)
        self.token = r.get("jwt")

    def get_stacks(self) -> dict:
        return self.request("api/endpoints/1/stacks")

    def get_stack(self, stack_id) -> dict:
        return self.request(f"api/endpoints/1/stacks/{stack_id}")

    def stack_with_name(self, name) -> dict:
        stacks = self.get_stacks()
        for stack in stacks:
            if stack.get("Name") == name:
                return stack
        raise LookupError(f"No stack with name '{name}'")

    def get_endpoints(self) -> dict:
        return self.request("api/endpoints")

    def get_env_vars(self, stack_id) -> dict:
        response = self.get_stack(stack_id)
        return {item["name"]: item["value"] for item in response["Env"]}

    def update_stack(
        self,
        stack_name: str,
        stack_file_content: str,
        env_vars: dict = None,
        prune: bool = False,
    ) -> dict:
        url = "api/endpoints/1/stacks/{}".format(stack_name)
        data = {
            "StackFileContent": stack_file_content,
            "Prune": prune,
            "Env": [{"name": k, "value": v} for k, v in env_vars.items()],
        }
        return self.request(url, method="PUT", data=data)

    def update_stack_with_file(
        self,
        stack_id: str,
        stack_file_path: str,
        env_vars: dict = None,
        prune: bool = False,
    ) -> dict:
        with open(stack_file_path, "r") as f:
            stack_file = f.read()
        return self.update_stack(stack_id, stack_file, env_vars=env_vars, prune=prune)

    def endpoints(self):
        return self.request("api/endpoints")

    def request(self, path: str, method: str = "GET", data: dict = None) -> dict:
        url = urljoin(self.host, path)
        headers = {}
        if self.token:
            headers["Authorization"] = "Bearer {}".format(self.token)
        response = requests.request(method, url, json=data, headers=headers)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.content
