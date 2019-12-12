import logging
import threading
from CredentialDatabase.dbhandler import DBHandler
from CredentialDatabase.exceptions import DBIntegrityError
import multiprocessing as mp
from multiprocessing.pool import ThreadPool

class CredentialFile():

    def __init__(self,  password_db=True):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class CredentialFile')

        # init base class
        #super().__init__(password_db, **dbparams)

        #self.file_path = filepath

    def start_iteration(self):
        """

        :return:
        """
        pass

    def read_file(self, file):
        """

        :param file:
        :return:
        """

        with open(file, mode='rb') as f:
            print(f.read(1024))

    def process_line(self, l):
        """

        :return:
        """
        #print(l)


if __name__ == '__main__':
    credfile = CredentialFile()
    credfile.read_file('/home/christian/projects/CredentialDatabase/Collections/rockyou.txt')
