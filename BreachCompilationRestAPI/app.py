#!/usr/bin/python3

from BreachCompilationRestAPI.routes.router import Router
from BreachCompilationRestAPI.routes.api_handler import APIHandler
from configparser import ConfigParser
from BreachCompilationRestAPI import ROOT_DIR

config = ConfigParser()
config.read(ROOT_DIR + '/config/cfg.ini')


class BreachCompilationRestAPI:

    def __init__(self, name, host, port, username, password, dbname):
        self.name = name

        self.api = APIHandler(host, port, username, password, dbname)

        self.router = Router(name=self.name)
        self.router.add_endpoint('/', 'index', method="GET", handler=self.api.index)
        self.router.add_endpoint('/api/passwords/', 'passwords', method="GET", handler=self.api.get_passwords)

    def run(self, port=None, debug=None):
        """

        :param port:
        :param debug:
        :return:
        """

        self.router.run(port=port, debug=debug)


def main():

    # load config settings
    host     = config.get('database', 'host')
    port     = config.getint('database', 'port')
    username = config.get('database', 'username')
    password = config.get('database', 'password')
    dbname   = config.get('database', 'dbname')

    # initialize BreachCompilationRestAPI app
    app = BreachCompilationRestAPI(name="BreachCompilationRestAPI", host=host, port=port, username=username,
                                   password=password, dbname=dbname)
    # run the app
    app.run()


if __name__ == '__main__':
    main()
