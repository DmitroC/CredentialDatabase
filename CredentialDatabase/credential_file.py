import logging
from itertools import islice
from multiprocessing import Pool

from CredentialDatabase.utils.password import Password
from CredentialDatabase.dbhandler import DBHandler
from CredentialDatabase.db.inserter import DBInserter
from CredentialDatabase.exceptions import DBIntegrityError


class CredentialFile(DBHandler):
    """ class CredentialFile to extract credentials from given file and insert into the database

    USAGE:
            credentialfile = CredentialFile(filepath=/tmp/example.txt, password_db=True, **dbparams)

    """
    def __init__(self, filepath, password_db=True, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class CredentialFile')

        # init base class
        super().__init__(password_db, **dbparams)

        # instances
        self.password = Password()
        self.dbinserter = DBInserter()

        self.filepath = filepath
        self.counter_passworddb = 1
        self.chars = set('0123456789abcdefghijklmnopqrstuvwxyz')

        # pool processes
        self.processes = 4
        self.filelines_divider = 1000000

    def start_iteration(self):
        """

        :return:
        """
        self.process_file()

    def one_thread_read_file(self):

        with open(self.filepath, mode='rb') as f:
            for line in f:
                try:
                    line = line.decode('utf-8').strip('\n')
                except UnicodeDecodeError as e:
                    line = line.decode('latin-1').strip('\n')
                self.insert_password_db(password=line)

    def insert_password_db(self, password):
        """ inserts password string into database table

        :param password: password string
        """

        if len(password) > 1:
            first_char_password = password[0].lower()
            second_char_password = password[1].lower()

            length_password = len(password)
            isSymbol = self.password.is_symbol(password)
            isNumber = self.password.is_number(password)

            if (first_char_password in self.chars) and (second_char_password in self.chars):
                data = (password, length_password, isNumber, isSymbol)
                query_str = "insert into \"{}\".\"{}\"(password, length, isnumber, issymbol) VALUES (%s, %s, %s, %s)".format(
                    first_char_password, second_char_password)
                try:
                    self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    self.counter_passworddb += 1
                    if (self.counter_passworddb % 1000) == 0:
                        self.logger.info("Database entry: " + str(data))
                except DBIntegrityError as e:
                    # self.logger.error(e)
                    pass
        else:
            # password to short
            self.logger.error("password to short: {}".format(password))

    def process_file(self):
        """ processes the file line numbers asynchronous with an Pool object

        """
        num_lines = self.get_lines_from_file()
        pool = Pool(processes=self.processes)

        end = 0
        while end < num_lines:
            if end == 0:
                start = 0
                end = self.filelines_divider
            else:
                start = end + 1
                end = start + (self.filelines_divider - 1)
            pool.apply_async(self.process_lines, args=(start, end))
        pool.close()
        pool.join()

    def get_lines_from_file(self):
        """ get the line number from the given filepath

        :return: int: number of lines
        """

        with open(self.filepath, mode='rb') as file:
            num_lines = sum(1 for line in file)
        return num_lines

    def process_lines(self, start, end):
        """ processes the line range from given start til the end

        :param start: start number of line
        :param end: end number of line
        """
        with open(self.filepath, mode='rb') as file:
            for line in islice(file, start, end):
                try:
                    line = line.decode('utf-8').strip('\n')
                except UnicodeDecodeError as e:
                    line = line.decode('latin-1').strip('\n')
                self.insert_password_db(password=line)


if __name__ == '__main__':
    import time
    start = time.time()
    credfile = CredentialFile('/home/christian/projects/CredentialDatabase/Collections/rockyou.txt')
    credfile.multiple_thread_read_file()
    end = time.time()
    print(end - start)
