import os
import logging
from CredentialDatabase.dbhandler import DBHandler


class BreachCompilation(DBHandler):
    """ class BreachCompilation to extract credentials from the BreachCompilation collection

    USAGE:
            breachcompilation = BreachCompilation()

    """
    def __init__(self, password_db=False, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class BreachCompilation')

        # init base class
        super().__init__(password_db, **dbparams)

        self.chars = set('0123456789abcdefghijklmnopqrstuvwxyz')

    def iterate_data_dir(self, folder):
        """ iterates over the data dir in the breachcompilation collection

        :param folder: path of the data folder
        """

        # check if it is a directory
        if os.path.isdir(folder):
            for elem in sorted(os.listdir(folder)):
                elem_abs = os.path.join(folder, elem)  # absolute path
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
            self.extract_cred_from_file(folder)

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
        print(email)
        if len(divide_email) == 2:
            username = divide_email[0]
            provider = divide_email[1]
            #sha1, sha256, sha512, md5 = generate_hashes(password)

            # insert in database
            #insert_data_in_db(email, password, username, provider, sha1, sha256, sha512, md5)
        else:
            self.logger.error("not_an_email: " + str(divide_email))

    def insert_data_in_db(self, email, password):
        pass

    def insert_password_in_db(self, password):

        first_char_password = password[0].lower()
        second_char_password = password[1].lower()
        length_password = len(password)
        isNumber = True
        isSymbol = True

        if first_char_password in self.chars:
            data = (id, password, length_password, isNumber, isSymbol)

            query_str = "insert into \"{}\".\"{}\"(id, password, length, isnumber, issymbol) VALUES (%s, %s, %s, %s, %s)".format(first_char_password, second_char_password)
            #self.dbinserter.row(sql=query_str, data=data)

        else:
            # handle symbols
            data = (id, password, length_password, isNumber, isSymbol)
            query_str = "insert into symbols.symbols(id, password, length, isnumber, issymbol) VALUES (%s, %s, %s, %s, %s)"
            #self.dbinserter.row(sql=query_str, data=data)


if __name__ == '__main__':
    breach = BreachCompilation()
    breach.iterate_data_dir(folder='/home/christian/projects/BreachCompilationRestAPI/BreachCompilation/data')
