import os
import logging
import threading
from multiprocessing import Process
from CredentialDatabase.dbhandler import DBHandler


class BreachCompilation(DBHandler):
    """ class BreachCompilation to extract credentials from the BreachCompilation collection

    USAGE:
            breachcompilation = BreachCompilation()

    """
    def __init__(self, folder_path, password_db=False, error_logs=False, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class BreachCompilation')

        # init base class
        super().__init__(password_db, **dbparams)

        self.breachcompilation_path = folder_path
        if 'data' not in os.listdir(self.breachcompilation_path):
            self.logger.error("no 'data' directory in given BreachCompilation path")
            raise FileNotFoundError

        self.data_folder = os.path.join(self.breachcompilation_path, 'data')
        self.error_logs = error_logs

    def start_iteration(self):
        """ starts the iteration worker processes

        """
        process = []
        for i, root_dir in enumerate(sorted(os.listdir(self.data_folder))):
            root_dir_abs = os.path.join(self.data_folder, root_dir)  # absolute path
            # start for each character folder one process
            proc = Process(target=self.iterate_data_dir, args=(root_dir_abs, ))
            process.append(proc)
            proc.start()

        for p in process:
            p.join()

    def start_thread_iteration(self):
        """ starts the iteration worker threads

        """
        threads = []
        for i, root_dir in enumerate(sorted(os.listdir(self.data_folder))):
            root_dir_abs = os.path.join(self.data_folder, root_dir)  # absolute path
            # start threads
            thread = threading.Thread(target=self.iterate_data_dir, args=(root_dir_abs,))
            threads.append(thread)
            thread.start()

        for t in threads:
            t.join()

    def iterate_data_dir(self, char_folder):
        """ iterates over the data dir in the breachcompilation collection

        :param char_folder: folder path for the specific character
        """

        # check if it is a directory
        if os.path.isdir(char_folder):
            for elem in sorted(os.listdir(char_folder)):
                elem_abs = os.path.join(char_folder, elem)  # absolute path
                if os.path.isdir(elem_abs):

                    # handle dir
                    for subelem in sorted(os.listdir(elem_abs)):
                        subelem_abs = os.path.join(elem_abs, subelem)
                        if os.path.isdir(subelem_abs):

                            # handle dir
                            pass
                        else:

                            # handle files
                            self.extract_cred_from_file(subelem_abs)
                else:
                    # handle files
                    self.extract_cred_from_file(elem_abs)

        else:
            # handle files
            self.extract_cred_from_file(char_folder)

    def extract_cred_from_file(self, file_path):
        """ extracts credentials from given file path

        :param file_path: path to file
        """

        with open(file_path, mode='rb') as file:
            self.logger.info("extract data from file " + str(file_path))

            # read all lines
            lines = file.readlines()
            try:
                for line in lines:
                    cred_list = line.decode('utf-8').rstrip('\n').split(':')
                    self.split_credentials(cred_list)
            except UnicodeDecodeError as e:
                for line in lines:
                    cred_list = line.decode('latin-1').rstrip('\n').split(':')
                    self.split_credentials(cred_list)

    def split_credentials(self, cred_list):
        """ splits the credentials in email and password

        :param cred_list:
        """

        if len(cred_list) == 2:
            email = cred_list[0]
            password = cred_list[1]
            self.prepare_credentials(email, password)

        elif len(cred_list) == 1:
            cred_list = cred_list[0].split(';')
            if len(cred_list) == 2:
                email = cred_list[0]
                password = cred_list[1]
                self.prepare_credentials(email, password)
            else:
                cred_list = cred_list[0].split(',')
                if len(cred_list) == 2:
                    email = cred_list[0]
                    password = cred_list[1]
                    self.prepare_credentials(email, password)

        elif len(cred_list) == 3:
            email = cred_list[0]
            password = cred_list[1]
            self.prepare_credentials(email, password)

        else:
            cred_list_length = len(cred_list)
            if self.error_logs:
                self.logger.error("array length  " + str(cred_list_length) + ": " + str(cred_list))

    def prepare_credentials(self, email, password):
        """ insert credentials in database

        :param email: email as string
        :param password: password as string
        """
        divide_email = email.split('@')

        if len(divide_email) == 2:
            if self.password_db:
                # insert in password database
                self.insert_password_db(password=password)
            else:
                # insert in breach database
                username = divide_email[0]
                provider = divide_email[1]
                self.insert_breach_db(email, password, username, provider)
        else:
            if self.error_logs:
                self.logger.error("got wrong format of email: {}".format(str(divide_email)))


