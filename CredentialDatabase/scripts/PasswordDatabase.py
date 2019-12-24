import logging
import argparse

from CredentialDatabase.utils.logger import Logger
from CredentialDatabase.breachcompilation import BreachCompilation
from CredentialDatabase.credential_file import CredentialFile


class PasswordDatabase:
    """ script PasswordDatabase to extract credentials from the BreachCompilation collection and insert it into the database

    USAGE:
            passworddb = PasswordDatabase(**dparams)

    """
    def __init__(self, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class PasswordDatabase')

        self.dbparams = dbparams

    def run(self, path, breach=False, proc=None):
        """ runs the password database script

        """
        if breach:
            breach = BreachCompilation(folder_path=path, password_db=True, **self.dbparams)
            breach.create_schemas_and_tables()
            breach.start_iteration()

        else:
            import time
            start = time.time()
            credfile = CredentialFile(filepath=path, password_db=True, num_proc=proc, **self.dbparams)
            credfile.create_schemas_and_tables()
            credfile.start_line_iteration()
            end = time.time()
            print("\n")
            print(end-start)


def main():

    # arguments
    parser = argparse.ArgumentParser(description="script to insert passwords in a database. \nUsage: PasswordDatabase "
                                                 "--host 192.168.1.2 --port 5432 --user john -password test1234 "
                                                 "--dbname postgres --breachpath /tmp/BreachCompilation (--filepath /path/to/credentialfile "
                                                 "--proc 10)")
    # database parameters
    parser.add_argument('--host',       type=str, help='hostname to connect to the database')
    parser.add_argument('--port',       type=str, help='port to connect to the database')
    parser.add_argument('--user',       type=str, help='user of the database')
    parser.add_argument('--password',   type=str, help='password from the user')
    parser.add_argument('--dbname',     type=str, help='database name')
    # breach compilation path
    parser.add_argument('--breachpath', type=str, help='path to the BreachCompilation collection folder')
    # password file path
    parser.add_argument('--filepath',   type=str, help='path to the credential file')
    # number of processes
    parser.add_argument('--proc',       type=int, help='number of processes')

    args = parser.parse_args()

    if (args.host and args.port and args.user and args.password and args.dbname) is None:
        print("Wrong number of arguments. Use it like: PasswordDatabase --host 192.168.1.2 --port 5432 --user "
              "john --password test1234 --dbname credentials --breachpath /path/to/BreachCompilation (--filepath /path/to/credentialfile "
              "--proc 10)")
        exit(1)
    else:
        host = args.host
        port = args.port
        username = args.user
        password = args.password
        dbname = args.dbname
        dbparams = {'host': host, 'port': port, 'username': username, 'password': password, 'dbname': dbname}

        # set up logger instance
        logger = Logger(name='CredentialDatabase', level='info', log_folder='/var/log/')
        logger.info("start script PasswordDatabase")
        print("start script PasswordDatabase")
        passworddb = PasswordDatabase(**dbparams)

        if (args.breachpath is not None) and (args.filepath is None):
            breachpath = args.breachpath
            passworddb.run(path=breachpath, breach=True)

        elif (args.filepath is not None) and (args.breachpath is None):
            filepath = args.filepath
            proc = args.proc
            passworddb.run(path=filepath, breach=False, proc=proc)

        else:
            print("please use either --breachpath or --filepath argument")
            exit(1)

        print("finished script PasswordDatabase")


if __name__ == '__main__':
    main()
