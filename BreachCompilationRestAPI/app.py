#!/usr/bin/python3

import argparse
from configparser import ConfigParser

from BreachCompilationRestAPI.routes.router import Router
from BreachCompilationRestAPI.routes.api_handler import APIHandler
from BreachCompilationRestAPI import ROOT_DIR

# load config file
config = ConfigParser()
config.read(ROOT_DIR + '/config/cfg.ini')


class BreachCompilationRestAPI:
    """ class BreachCompilationRestAPI to define the API and endpoint structure of this application

    USAGE:
            app = BreachCompilationRestAPI(name="BreachCompilationRestAPI", host=host, port=port, username=username,
                                           password=password, dbname=dbname)

            app.run()
    """
    def __init__(self, name, host, port, username, password, dbname):
        self.name = name

        # defines the api handler methods
        self.api = APIHandler(host, port, username, password, dbname)

        # router instance for specific endpoints
        self.router = Router(name=self.name)
        self.router.add_endpoint('/', 'index', method="GET", handler=self.api.index)
        self.router.add_endpoint('/api/passwords/', 'passwords', method="GET", handler=self.api.get_passwords)

    def run(self, host='0.0.0.0', port=None, debug=None):
        """ runs the BreachCompilationRestAPI application on given port

        :param host: default hostname
        :param port: port for the webserver
        :param debug: debug mode true or false
        """

        self.router.run(host=host, port=port, debug=debug)


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
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()
