import logging
import threading
from CredentialDatabase.db.connector import DBConnector
from CredentialDatabase.db.creator import DBCreator
from CredentialDatabase.db.fetcher import DBFetcher
from CredentialDatabase.db.inserter import DBInserter


class DBHandler:
    """ class DBHandler to provide database actions to subclasses

    USAGE:
            dbhandler = DBHandler()

    """
    def __init__(self, password_db, **dbparams):
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

        self.dbcreator = DBCreator()
        self.dbfetcher = DBFetcher()
        self.dbinserter = DBInserter()

        # database schema structure
        self.dbstructure = '0123456789abcdefghijklmnopqrstuvwxyz'
        self.schema_list = list(self.dbstructure)
        self.schema_list.append('symbols')

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
                table_sql = "create table if not exists \"{}\".symbols (password text primary key, length bigint, isNumber boolean, isSymbol boolean);".format(
                    schema)
            else:
                table_sql = "create table if not exists \"{}\".symbols (id bigint primary key, email text, password text, username text, provider text, sha1 varchar(40), sha256 varchar(64), sha512 varchar(128), md5 varchar(32));".format(
                    schema)
            self.dbinserter.sql(sql=table_sql)
        else:
            for table in self.schema_list:
                if self.password_db:
                    table_sql = "create table if not exists \"{}\".\"{}\" (password text primary key, length bigint, isNumber boolean, isSymbol boolean);".format(
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
