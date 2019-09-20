from configparser import ConfigParser
from BreachCompilationRestAPI import ROOT_DIR
from BreachCompilationRestAPI.app import BreachCompilationRestAPI

config = ConfigParser()
config.read(ROOT_DIR + '/config/cfg.ini')


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
