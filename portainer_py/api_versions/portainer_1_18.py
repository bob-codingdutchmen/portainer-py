from .portainer_1_17 import Portainer_1_17


class Portainer_1_18(Portainer_1_17):
    FROM_VERSION = (1, 18)
    URL_STACKS = "api/stacks"
    URL_STACK = "api/stacks/{stack_id}?endpointId=1"


