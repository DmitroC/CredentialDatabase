from BreachCompilationRestAPI.routes.router import Router
from BreachCompilationRestAPI.routes.api_handler import APIHandler


class BreachCompilationRestAPI:

    def __init__(self, name):
        self.name = name

        self.api = APIHandler()

        self.router = Router(name=self.name)
        self.router.add_endpoint('/api/passwords/', 'passwords', method="GET", handler=self.api.get_passwords)

    def run(self, port=None, debug=None):
        """

        :param port:
        :param debug:
        :return:
        """

        self.router.run(port=port, debug=debug)
