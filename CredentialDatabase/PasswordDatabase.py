import logging
import argparse

from CredentialDatabase.utils.logger import Logger
from CredentialDatabase.breachcompilation import BreachCompilation


class PasswordDatabase:

    def __init__(self, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class PasswordDatabase')

        self.breach = BreachCompilation(password_db=True, **dbparams)
        self.breach.create_schemas_and_tables()


def main():

    # arguments
    parser = argparse.ArgumentParser(description="script to insert passwords in a database")
    parser.add_argument('--host',     type=str, help='hostname to connect to the database')
    parser.add_argument('--port',     type=str, help='port to connect to the database')
    parser.add_argument('--user',     type=str, help='user of the database')
    parser.add_argument('--password', type=str, help='password from the user')
    parser.add_argument('--dbname',   type=str, help='database name')
    #parser.add_argument('--path',     type=str, help='path to BreachCompilation Collection')

    args = parser.parse_args()

    if (args.host and args.port and args.user and args.password and args.dbname) is None:
        print("Wrong number of arguments. Use it like: ./PasswordDatabase.py --host 192.168.1.2 --port 5432 --user "
              "john --password test1234 --dbname credentials --path /path/to/BreachCompilation")
        exit(1)
    else:
        print("start script PasswordDatabase")
        host = args.host
        port = args.port
        username = args.user
        password = args.password
        dbname = args.dbname
        dbparams = {'host': host, 'port': port, 'username': username, 'password': password, 'dbname': dbname}

        # set up logger instance
        logger = Logger(name='CredentialDatabase', level='info', log_folder='/var/log/')
        logger.info("start script PasswordDatabase")

        password = PasswordDatabase(**dbparams)

        print("finished script PasswordDatabase")


if __name__ == '__main__':
    main()
