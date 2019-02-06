import json


class PortainerError(IOError):
    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        try:
            self.message = response.json()['err']
        except json.JSONDecodeError:
            self.message = response.content.decode("utf-8")
        super(PortainerError, self).__init__(*args, **kwargs)
