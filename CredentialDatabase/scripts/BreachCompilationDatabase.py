import logging
import argparse
from CredentialDatabase.utils.logger import Logger
from CredentialDatabase.breachcompilation import BreachCompilation


class BreachCompilationDatabase:
    """ script BreachCompilationDatabase to extract credentials from the BreachCompilation collection and insert it into the database

    USAGE:
            breachcompilation = BreachCompilationDatabase(breachpath=/tmp/, **dparams)

    """
    def __init__(self, breachpath, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class BreachCompilationDatabase')

        self.breach = BreachCompilation(folder_path=breachpath, password_db=False, **dbparams)
        self.breach.create_schemas_and_tables()
        self.breach.start_iteration()


def main():

    # arguments
    parser = argparse.ArgumentParser(description="script to insert BreachCompilation credentials into postgresql database. "
                                                 "\nUsage: PasswordDatabase --host 192.168.1.2 --port 5432 --user john "
                                                 "-password test1234 --dbname postgres --breachpath /tmp/BreachCompilation")

    parser.add_argument('--host',       type=str, help='hostname to connect to the database')
    parser.add_argument('--port',       type=str, help='port to connect to the database')
    parser.add_argument('--user',       type=str, help='user of the database')
    parser.add_argument('--password',   type=str, help='password from the user')
    parser.add_argument('--dbname',     type=str, help='database name')
    parser.add_argument('--breachpath', type=str, help='path to the BreachCompilation Collection')

    args = parser.parse_args()

    if (args.host and args.port and args.user and args.password and args.dbname and args.breachpath) is None:
        print("Wrong number of arguments. Use it like: BreachCompilationDatabase --host 192.168.1.2 --port 5432 --user "
              "john --password test1234 --dbname breachcompilation --breachpath /path/to/BreachCompilation")
        exit(1)
    else:
        print("start script BreachCompilationDatabase")
        host = args.host
        port = args.port
        username = args.user
        password = args.password
        dbname = args.dbname
        breachpath = args.breachpath
        dbparams = {'host': host, 'port': port, 'username': username, 'password': password, 'dbname': dbname}

        # set up logger instance
        logger = Logger(name='CredentialDatabase', level='info', log_folder='/var/log/')
        logger.info("start script BreachCompilationDatabase")

        breachcompilationdb = BreachCompilationDatabase(breachpath=breachpath, **dbparams)

        print("finished script BreachCompilationDatabase")


if __name__ == '__main__':
    main()
