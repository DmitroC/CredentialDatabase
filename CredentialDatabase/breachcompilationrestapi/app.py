#!/usr/bin/python3

import argparse
from configparser import ConfigParser

from CredentialDatabase.breachcompilationrestapi.routes.router import Router
from CredentialDatabase.breachcompilationrestapi.routes.api import APIHandler
from BreachCompilationRestAPI.utils.logger import Logger
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

    # set up logger instance
    logger = Logger(name='BreachCompilationRestAPI', level='info', log_folder='var/log/', debug=True)
    logger.info("start application BreachCompilationRestAPI")

    # arguments
    parser = argparse.ArgumentParser(description="arguments for BreachCompilationApp")
    parser.add_argument('--host', type=str, help='hostname to connect to the database')
    parser.add_argument('--port', type=str, help='port to connect to the database')
    parser.add_argument('--user', type=str, help='user of the database')
    parser.add_argument('--password', type=str, help='password from user')
    parser.add_argument('--dbname', type=str, help='database name')
    parser.add_argument('--schema', type=str, help='schema name')
    parser.add_argument('--app-host', type=str, help='hostname for the application')
    parser.add_argument('--app-port', type=str, help='port for the application')
    args = parser.parse_args()

    if (args.host and args.port and args.user and args.password and args.dbname) is None:
        print("load settings from config file")
        # load config settings
        host     = config.get('database', 'host')
        port     = config.getint('database', 'port')
        username = config.get('database', 'username')
        password = config.get('database', 'password')
        dbname   = config.get('database', 'dbname')
        schema = config.get('database', 'schema')

    else:
        host     = args.host
        port     = args.port
        username = args.user
        password = args.password
        dbname   = args.dbname
        schema   = args.schema

    if args.app_host is None:
        app_host = '0.0.0.0'
    else:
        app_host = args.app_host

    if args.app_port is None:
        app_port = 5000
    else:
        app_port = args.app_port

    # initialize BreachCompilationRestAPI app
    app = BreachCompilationRestAPI(name="BreachCompilationRestAPI", host=host, port=port, username=username,
                                   password=password, dbname=dbname)
    # run the app
    app.run(host=app_host, port=app_port, debug=False)


if __name__ == '__main__':
    main()
