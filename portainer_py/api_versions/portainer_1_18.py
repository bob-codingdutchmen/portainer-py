from .portainer_1_17 import Portainer_1_17


class Portainer_1_18(Portainer_1_17):
    FROM_VERSION = (1, 18)

    def get_stacks(self):
        return self.request("api/stacks")

    def get_stack(self, stack_id) -> dict:
        return self.request(f"api/stacks/{stack_id}")

