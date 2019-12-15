import string
import logging
import hashlib


class Password:
    """ class Password to provide methods for password analysing

    USAGE:
            password = Password()

    """
    def __init__(self):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class Password')

        self.all_normal_char = string.ascii_letters + string.digits

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

    def generate_hashes(self, password):
        """ generates the hash of given password string

        :param password: password string
        :return: sh1, sh256, sha512, md5
        """
        sha1 = hashlib.sha1(password.encode()).hexdigest()      # 40
        sha256 = hashlib.sha256(password.encode()).hexdigest()  # 64
        sha512 = hashlib.sha512(password.encode()).hexdigest()  # 128
        md5 = hashlib.md5(password.encode()).hexdigest()        # 32

        return sha1, sha256, sha512, md5
