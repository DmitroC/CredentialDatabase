#!/usr/bin/python3

import os
import logging
import hashlib
import threading
import argparse
import psycopg2
from psycopg2 import pool
from logging.handlers import RotatingFileHandler

# set up logger
trace_logger = logging.getLogger('trace_logger')
trace_logger.setLevel(logging.INFO)
insertfail_logger = logging.getLogger('insertfail_logger')
insertfail_logger.setLevel(logging.WARNING)
file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.INFO)

counter = dict()
structure = '0123456789abcdefghijklmnopqrstuvwxyz'
chars = set('0123456789abcdefghijklmnopqrstuvwxyz')
for i in chars:
    counter.update({i: 1})
counter_sym = 1
counter_pass = 1


def formate_logger():

    # log directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(current_dir, 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # formatter and handler
    formatter = logging.Formatter('%(asctime)s - %(lineno)d@%(filename)s - %(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    trace_rotate_handler = RotatingFileHandler(log_dir + '/trace.log', mode='a', maxBytes=20000000, backupCount=5)
    trace_rotate_handler.setFormatter(formatter)
    trace_rotate_handler.setLevel(logging.INFO)

    insertfail_rotate_handler = RotatingFileHandler(log_dir + '/insert_fail.log', mode='a', maxBytes=20000000, backupCount=5)
    insertfail_rotate_handler.setFormatter(formatter)
    insertfail_rotate_handler.setLevel(logging.WARNING)

    file_rotate_handler = RotatingFileHandler(log_dir + '/file.log', mode='a', maxBytes=20000000, backupCount=5)
    file_rotate_handler.setFormatter(formatter)
    file_rotate_handler.setLevel(logging.INFO)

    # add handler
    trace_logger.addHandler(stream_handler)
    trace_logger.addHandler(trace_rotate_handler)
    insertfail_logger.addHandler(stream_handler)
    insertfail_logger.addHandler(insertfail_rotate_handler)
    file_logger.addHandler(stream_handler)
    file_logger.addHandler(file_rotate_handler)


def db_conn_pool(host, port, user, password, dbname):
    trace_logger.info("connecting to database")
    global threaded_postgresql_pool
    threaded_postgresql_pool = psycopg2.pool.ThreadedConnectionPool(10, 40, user=user, password=password,
                                                                    host=host, port=port, database=dbname)

def create_schemas_and_tables():
    trace_logger.info("create schemas and tables for breachcompilation credentials")

    # database options
    table_conn = threaded_postgresql_pool.getconn()
    cursor = table_conn.cursor()

    schema_struct = list(structure)
    schema_struct.append('symbols')
    for schema in schema_struct:
        schema_sql = "create schema if not exists \"{}\"".format(schema)
        cursor.execute(schema_sql)
        table_conn.commit()
        if schema == 'symbols':
            table_sql = "create table if not exists \"{}\".symbols (id bigint primary key, email text, password text, username text, provider text, sha1 varchar(40), sha256 varchar(64), sha512 varchar(128), md5 varchar(32));".format(schema)
            cursor.execute(table_sql)
            table_conn.commit()
        else:
            for table in schema_struct:
                table_sql = "create table if not exists \"{}\".\"{}\" (id bigint primary key, email text, password text, username text, provider text, sha1 varchar(40), sha256 varchar(64), sha512 varchar(128), md5 varchar(32));".format(schema, table)
                cursor.execute(table_sql)
                table_conn.commit()

def iterate_data_root_dir(breach_compilation_path):

    # check if path includes data directory
    if 'data' not in os.listdir(breach_compilation_path):
        print("no 'data' directory in given BreachCompilation path")
        trace_logger.info("no 'data' directory in given BreachCompilation path")
        return

    breach_compilation_path_data = os.path.join(breach_compilation_path, 'data')
    threads = []
    for i, root_dir in enumerate(sorted(os.listdir(breach_compilation_path_data))):
        root_dir_abs = os.path.join(breach_compilation_path_data, root_dir)  # absolute path
        # start threads
        thread = threading.Thread(target=folder_worker_thread, args=(root_dir_abs,))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()


def folder_worker_thread(folder_path):

    # check if it is a directory
    if os.path.isdir(folder_path):
        for elem in sorted(os.listdir(folder_path)):
            elem_abs = os.path.join(folder_path, elem)  # absolute path
            if os.path.isdir(elem_abs):
                # handle dir
                for subelem in sorted(os.listdir(elem_abs)):
                    subelem_abs = os.path.join(elem_abs, subelem)
                    if os.path.isdir(subelem_abs):
                        # handle dir
                        pass
                    else:
                        # handle files
                        extract_cred_from_file(subelem_abs)
            else:
                # handle files
                extract_cred_from_file(elem_abs)

    else:
        # handle files
        extract_cred_from_file(folder_path)


def extract_cred_from_file(file_path):

    with open(file_path, mode='rb') as file:
        file_logger.info("extract data from file " + str(file_path))
        # read all lines
        lines = file.readlines()
        try:
            for line in lines:
                cred_list = line.decode('utf-8').rstrip('\n').split(':')
                splitter(cred_list)
        except UnicodeDecodeError as e:
            for line in lines:
                cred_list = line.decode('latin-1').rstrip('\n').split(':')
                splitter(cred_list)


def splitter(cred_list):

    if len(cred_list) == 2:
        email = cred_list[0]
        password = cred_list[1]
        handle_credentials(email, password)

    elif len(cred_list) == 1:
        cred_list = cred_list[0].split(';')
        if len(cred_list) == 2:
            email = cred_list[0]
            password = cred_list[1]
            handle_credentials(email, password)
        else:
            cred_list = cred_list[0].split(',')
            if len(cred_list) == 2:
                email = cred_list[0]
                password = cred_list[1]
                handle_credentials(email, password)
    else:
        cred_list_length = len(cred_list)
        insertfail_logger.error("len: " + str(cred_list_length) + ": " + str(cred_list))


def handle_credentials(email, password):

    divide_email = email.split('@')

    if len(divide_email) == 2:
        username = divide_email[0]
        provider = divide_email[1]
        sha1, sha256, sha512, md5 = generate_hashes(password)

        # insert in database
        insert_data_in_db(email, password, username, provider, sha1, sha256, sha512, md5)
    else:
        insertfail_logger.error("not_an_email: " + str(divide_email))


def generate_hashes(password):

    sha1 = hashlib.sha1(password.encode()).hexdigest() # 40
    sha256 = hashlib.sha256(password.encode()).hexdigest() # 64
    sha512 = hashlib.sha512(password.encode()).hexdigest() # 128
    md5 = hashlib.md5(password.encode()).hexdigest() # 32

    return sha1, sha256, sha512, md5


def insert_data_in_db(email, password, username, provider, sha1, sha256, sha512, md5):
    global counter, counter_sym
    first_char_email = email[0].lower()
    second_char_email = email[1].lower()
    chars = set('0123456789abcdefghijklmnopqrstuvwxyz')

    if first_char_email in chars:

        data = (counter[first_char_email], str(email), str(password), str(username), str(provider), str(sha1), str(sha256), str(sha512), str(md5))
        char_conn = threaded_postgresql_pool.getconn(key=first_char_email)
        cursor = char_conn.cursor()

        try:
            query_str = "insert into \"{}\".\"{}\"(id, email, password, username, provider, sha1, sha256, sha512, md5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(first_char_email, second_char_email)

            cursor.execute(query_str, data)
            char_conn.commit()
            counter[first_char_email] += 1
            if (data[0] % 1000) == 0:
                trace_logger.info("inserted: " + str(data))

        except psycopg2.errors.UniqueViolation as e:
            counter[first_char_email] += 1
            insertfail_logger.error(e)

        except Exception as e:
            # save data which are not inserted
            insertfail_logger.error(e)
            char_conn.commit()

    else:
        # handle symbols
        data = (counter_sym, str(email), str(password), str(username), str(provider), str(sha1), str(sha256), str(sha512), str(md5))
        sym_conn = threaded_postgresql_pool.getconn(key='symbols')
        cursor = sym_conn.cursor()

        try:
            query_str = "insert into symbols.symbols(id, email, password, username, provider, sha1, sha256, sha512, md5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_str, data)
            sym_conn.commit()

            counter_sym += 1
            if (counter_sym % 1000) == 0:
                trace_logger.info("inserted: " + str(data))

        except psycopg2.errors.UniqueViolation as e:
            counter[first_char_email] += 1
            insertfail_logger.error(e)

        except Exception as e:
            # save data which are not inserted
            insertfail_logger.error(e)
            insertfail_logger.error(str(data))
            sym_conn.commit()


def main():

    # arguments
    parser = argparse.ArgumentParser(description="script to insert BreachCompilation credentials into postgresql database")
    parser.add_argument('--host', type=str, help='hostname to connect database')
    parser.add_argument('--port', type=str, help='port to connect database')
    parser.add_argument('--user', type=str, help='user of database')
    parser.add_argument('--password', type=str, help='password from user')
    parser.add_argument('--dbname', type=str, help='database name')
    parser.add_argument('--path', type=str, help='path to BreachCompilation Collection')

    args = parser.parse_args()

    if (args.host and args.port and args.user and args.password and args.dbname and args.path) is None:
        print("Wrong number of arguments. Use it like: ./BreachCompilationDatabase_old.py --host 192.168.1.2 --port 5432 --user "
              "john --password test1234 --dbname credentials --schema breachcompilation --path /path/to/BreachCompilation")
        exit(1)
    else:
        print("start script BreachCompilationDatabase_old.py")

        # create loggers
        formate_logger()

        # connecting to database pool
        db_conn_pool(args.host, args.port, args.user, args.password, args.dbname)

        # check and create schema as well as all tables in database
        create_schemas_and_tables()

        # creates for each directory a worker thread to extract all credentials
        iterate_data_root_dir(args.path)


if __name__ == '__main__':
    main()
