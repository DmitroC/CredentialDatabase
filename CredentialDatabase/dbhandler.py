import time
import logging
import threading
from CredentialDatabase.db.connector import DBConnector
from CredentialDatabase.db.creator import DBCreator
from CredentialDatabase.db.fetcher import DBFetcher
from CredentialDatabase.db.inserter import DBInserter
from CredentialDatabase.utils.password import Password
from CredentialDatabase.exceptions import DBIntegrityError


class DBHandler:
    """ class DBHandler to provide database actions to subclasses

    USAGE:
            dbhandler = DBHandler()

    """
    def __init__(self, password_db, db_entries_logger=1000, **dbparams):
        self.logger = logging.getLogger('CredentialDatabase')
        self.logger.info('create class DBHandler')

        self.password_db = password_db

        if ('host' and 'port' and 'username' and 'password' and 'dbname') in dbparams.keys():
            self.db_host = dbparams['host']
            self.db_port = dbparams['port']
            self.db_username = dbparams['username']
            self.db_password = dbparams['password']
            self.db_name = dbparams['dbname']
        else:
            self.logger.error("no database params provided!")

        DBConnector.connect_psycopg(host=self.db_host, port=self.db_port, username=self.db_username,
                                    password=self.db_password, dbname=self.db_name, minConn=1, maxConn=39)

        # database instances
        self.dbcreator = DBCreator()
        self.dbfetcher = DBFetcher()
        self.dbinserter = DBInserter()

        # instances
        self.password = Password()

        # database schema structure
        self.dbstructure = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.schema_list = list(self.dbstructure)
        self.schema_list.append('symbols')
        self.counter_passworddb = 1
        self.chars = set('0123456789abcdefghijklmnopqrstuvwxyz')
        self.db_entries_logger = db_entries_logger

        self.counter = dict()
        for i in self.chars:
            self.counter.update({i: 1})
        self.counter_sym = 1

        # threads
        self.threads = []

    def create_schemas_and_tables(self, remove=False):
        """ creates schemas and tables in database

        """
        self.logger.info("create schemas and tables in database")
        # start threads
        for schema in self.schema_list:
            if remove:
                thread = threading.Thread(target=self.remove_schema_worker, args=(schema,))
            else:
                thread = threading.Thread(target=self.schema_worker, args=(schema,))
            self.threads.append(thread)
            thread.start()

        for t in self.threads:
            t.join()

    def schema_worker(self, schema):
        """ worker to create the schemas and tables in the database

        :param schema: specific schema
        """
        self.logger.info("create schema {}".format(schema))
        schema_sql = "create schema if not exists \"{}\"".format(schema)
        self.dbinserter.sql(sql=schema_sql)

        if schema == 'symbols':
            if self.password_db:
                table_sql = "create table if not exists \"{}\".symbols (password text primary key, length bigint, isNumber boolean, isSymbol boolean, ts text);".format(
                    schema)
            else:
                table_sql = "create table if not exists \"{}\".symbols (id bigint primary key, email text, password text, username text, provider text, sha1 varchar(40), sha256 varchar(64), sha512 varchar(128), md5 varchar(32));".format(
                    schema)
            self.dbinserter.sql(sql=table_sql)
        else:
            for table in self.schema_list:
                if self.password_db:
                    table_sql = "create table if not exists \"{}\".\"{}\" (password text primary key, length bigint, isNumber boolean, isSymbol boolean, ts text);".format(
                        schema, table)
                else:
                    table_sql = "create table if not exists \"{}\".\"{}\" (id bigint primary key, email text, password text, username text, provider text, sha1 varchar(40), sha256 varchar(64), sha512 varchar(128), md5 varchar(32));".format(
                        schema, table)
                self.dbinserter.sql(sql=table_sql)

    def remove_schema_worker(self, schema):
        """ worker to remove the schemas and tables in the database

        """
        self.logger.info("remove schema {}".format(schema))
        drop_schema_sql = "drop schema \"{}\" cascade".format(schema)
        self.dbinserter.sql(sql=drop_schema_sql)

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
            utc_ts = str(time.time()).split('.')[0]

            if (first_char_password in self.chars) and (second_char_password in self.chars):
                data = (password, length_password, isNumber, isSymbol, utc_ts)
                query_str = "insert into \"{}\".\"{}\"(password, length, isnumber, issymbol, ts) VALUES (%s, %s, %s, %s, %s)".format(
                    first_char_password, second_char_password)
                try:
                    self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    self.counter_passworddb += 1
                    if (self.counter_passworddb % self.db_entries_logger) == 0:
                        self.logger.info("Database entry {}: {}".format(self.counter_passworddb, str(data)))
                except DBIntegrityError as e:
                    # self.logger.error(e)
                    pass
            else:
                # handle symbols
                data = (password, length_password, isNumber, isSymbol, utc_ts)
                query_str = "insert into symbols.symbols(password, length, isnumber, issymbol, ts) VALUES (%s, %s, %s, %s, %s)"
                try:
                    self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    self.counter_passworddb += 1
                    if (self.counter_passworddb % self.db_entries_logger) == 0:
                        self.logger.info("Database entry {}: {}".format(self.counter_passworddb, str(data)))
                except DBIntegrityError as e:
                    # self.logger.error(e)
                    pass
        else:
            # password to short
            #self.logger.error("password to short for this database structure: {}".format(password))
            pass

    def insert_breach_db(self, email, password, username, provider):
        """ inserts data from the breachcompilation collection into the database

        :param email: email string
        :param password: password string
        :param username: username from email
        :param provider: provider from email
        :param sha1: sha1 hash
        :param sha256: sha256 hash
        :param sha512: sha512 hash
        :param md5: md5 hash

        """
        if len(email) > 1:
            first_char_email = email[0].lower()
            second_char_email = email[1].lower()
            sha1, sha256, sha512, md5 = self.password.generate_hashes(password=password)

            if (first_char_email in self.chars) and (second_char_email in self.chars):
                data = (self.counter[first_char_email], str(email), str(password), str(username), str(provider), str(sha1), str(sha256), str(sha512), str(md5))
                try:
                    query_str = "insert into \"{}\".\"{}\"(id, email, password, username, provider, sha1, sha256, sha512, md5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(first_char_email, second_char_email)
                    self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    self.counter[first_char_email] += 1

                    if (self.counter[first_char_email] % self.db_entries_logger) == 0:
                        self.logger.info("Database entry {}: {}".format(self.counter[first_char_email], str(data)))

                except DBIntegrityError as e:
                    #self.counter[first_char_email] += 1
                    self.logger.error(e)

                except Exception as e:
                    # save data which are not inserted
                    self.logger.error(e)
            else:
                # handle symbols
                data = (self.counter_sym, str(email), str(password), str(username), str(provider), str(sha1), str(sha256), str(sha512), str(md5))

                try:
                    query_str = "insert into symbols.symbols(id, email, password, username, provider, sha1, sha256, sha512, md5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    self.dbinserter.row(sql=query_str, data=data, autocommit=True)
                    self.counter_sym += 1

                    if (self.counter_sym % self.db_entries_logger) == 0:
                        self.logger.info("Database entry {}: {}".format(self.counter_sym, str(data)))

                except DBIntegrityError as e:
                    #self.counter[first_char_email] += 1
                    self.logger.error(e)

                except Exception as e:
                    # save data which are not inserted
                    self.logger.error(e)
        else:
            #self.logger.error("email to short for this database structure: {}".format(email))
            pass
