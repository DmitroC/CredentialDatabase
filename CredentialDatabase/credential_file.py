import math
import logging
from itertools import islice
from multiprocessing import Process
from CredentialDatabase.dbhandler import DBHandler


class CredentialFile(DBHandler):
    """ class CredentialFile to extract credentials from given file and insert into the database

    USAGE:
            credentialfile = CredentialFile(filepath=/tmp/example.txt, password_db=True, num_proc=10, **dbparams)

    """

    def __init__(self, filepath, password_db=True, num_proc=10, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class CredentialFile')

        # init base class
        super().__init__(password_db=password_db, db_entries_logger=1000, **dbparams)

        self.filepath = filepath
        if num_proc is None:
            self.num_proc = 10
        else:
            self.num_proc = num_proc

    def calc_lines_per_process(self, num_lines):
        """ calculates the number of lines for each process

        :return:
        """
        return math.ceil(num_lines / self.num_proc)

    def start_line_iteration(self):
        """ starts the line iteration

        """
        num_lines = self.get_lines_from_file()
        end = 0
        self.logger.info("file contains {} number of lines".format(num_lines))

        # calc lines per process
        lines_per_process = self.calc_lines_per_process(num_lines)

        process = []
        while end < num_lines:
            if end == 0:
                start = 0
                end = lines_per_process
            else:
                start = end + 1
                end = start + (lines_per_process - 1)
            proc = Process(target=self.process_lines, args=(start, end,))
            process.append(proc)
            proc.start()

        if len(process) == 1:
            self.logger.info("created {} process for this task".format(len(process)))
        else:
            self.logger.info("created {} processes for this task".format(len(process)))

        for proc in process:
            proc.join()

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
                    line = line.decode('utf-8').strip('\r\n')
                except UnicodeDecodeError as e:
                    line = line.decode('latin-1').strip('\r\n')
                self.insert_password_db(password=line)

