import os
import string
import logging
import threading
from CredentialDatabase.dbhandler import DBHandler
from CredentialDatabase.exceptions import DBIntegrityError


class BreachCompilation(DBHandler):
    """ class BreachCompilation to extract credentials from the BreachCompilation collection

    USAGE:
            breachcompilation = BreachCompilation()

    """
    def __init__(self, folder_path, password_db=False, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class BreachCompilation')

        # init base class
        super().__init__(password_db, **dbparams)

        self.chars = set('0123456789abcdefghijklmnopqrstuvwxyz')
        self.all_normal_char = string.ascii_letters + string.digits

        self.breachcompilation_path = folder_path
        if 'data' not in os.listdir(self.breachcompilation_path):
            self.logger.error("no 'data' directory in given BreachCompilation path")
            raise FileNotFoundError

        self.data_folder = os.path.join(self.breachcompilation_path, 'data')

    def start_iteration(self):
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

        :param folder: path of the data folder
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
            self.logger.error("len: " + str(cred_list_length) + ": " + str(cred_list))

    def prepare_credentials(self, email, password):
        """ insert credentials in database

        :param email: email as string
        :param password: password as string
        """
        divide_email = email.split('@')

        if len(divide_email) == 2:
            username = divide_email[0]
            provider = divide_email[1]
            #sha1, sha256, sha512, md5 = generate_hashes(password)

            if self.password_db:
                self.insert_data_in_db(email=None, password=password)
            else:
                # insert in database
                #self.insert_data_in_db(email, password, username, provider, sha1, sha256, sha512, md5)
                pass
        else:
            self.logger.error("not_an_email: " + str(divide_email))

    def is_number(self, password):
        """ checks if the password contains a number

        :param password: string
        :return: True of False
        """
        return any(char.isdigit() for char in password)

    def is_symbol(self, password):
        """ checks if the password contains a symbol

        :param password: string
        :return: True or False
        """

        spec_char = [char for char in password if char not in self.all_normal_char]
        if len(spec_char) > 0:
            return True
        else:
            return False

    def insert_data_in_db(self, email, password):
        """

        :param email:
        :param password:
        :return:
        """

        if email is None:
            if len(password) > 1:
                first_char_password = password[0].lower()
                second_char_password = password[1].lower()

                length_password = len(password)
                isNumber = self.is_number(password)
                isSymbol = self.is_symbol(password)

                if (first_char_password in self.chars) and (second_char_password in self.chars):
                    data = (password, length_password, isNumber, isSymbol)
                    self.logger.info(data)
                    query_str = "insert into \"{}\".\"{}\"(password, length, isnumber, issymbol) VALUES (%s, %s, %s, %s)".format(
                        first_char_password, second_char_password)
                    try:
                        self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    except DBIntegrityError as e:
                        self.logger.error(e)
                        pass
                else:
                    # handle symbols
                    data = (password, length_password, isNumber, isSymbol)
                    self.logger.info(data)
                    query_str = "insert into symbols.symbols(password, length, isnumber, issymbol) VALUES (%s, %s, %s, %s)"
                    try:
                        self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    except DBIntegrityError as e:
                        self.logger.error(e)
                        pass


if __name__ == '__main__':
    breach = BreachCompilation(folder_path='/home/christian/projects/BreachCompilationRestAPI/BreachCompilation/')
    breach.start_iteration()
