#!/usr/bin/python3

import os
import logging
from logging.handlers import RotatingFileHandler
import argparse
import psycopg2
from string import ascii_lowercase

# set up logger
trace_logger = logging.getLogger('trace_logger')
trace_logger.setLevel(logging.INFO)
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.WARNING)
counter = 1


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
    trace_rotate_handler = RotatingFileHandler(log_dir + '/trace.log', mode='a', maxBytes=30000000)
    trace_rotate_handler.setFormatter(formatter)
    trace_rotate_handler.setLevel(logging.INFO)

    error_rotate_handler = RotatingFileHandler(log_dir + '/insert_fail.log', mode='a', maxBytes=30000000)
    error_rotate_handler.setFormatter(formatter)
    error_rotate_handler.setLevel(logging.WARNING)

    # add handler
    trace_logger.addHandler(stream_handler)
    trace_logger.addHandler(trace_rotate_handler)
    error_logger.addHandler(stream_handler)
    error_logger.addHandler(error_rotate_handler)


def connect_db(host, port, user, password, dbname):
    print("connecting to database")
    global db_conn
    global cursor
    db_conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
    cursor = db_conn.cursor()
    trace_logger.info("connecting to postgresql database")


def create_table():
    trace_logger.info("create schema/table for breach compilation credentials")

    query_schema = "create schema if not exists breach_compilation;"
    cursor.execute(query_schema)
    db_conn.commit()

    # tables for numbers
    for i in range(10):
        #query_table = "create table if not exists breach_compilation.\"{}\" (id bigint, email text primary key, password text, username text, provider text);".format(i)
        query_table = "create table if not exists breach_compilation.\"{}\" (id bigint, email text, password text, username text, provider text);".format(i)
        cursor.execute(query_table)
        db_conn.commit()

    # tables for letters
    for c in ascii_lowercase:
        query_table = "create table if not exists breach_compilation.\"{}\" (id bigint, email text, password text, username text, provider text);".format(c)
        cursor.execute(query_table)
        db_conn.commit()

    # table for symbols
    query_table = "create table if not exists breach_compilation.symbols (id bigint, email text, password text, username text, provider text);"
    cursor.execute(query_table)
    db_conn.commit()


def insert_data_in_db(data):
    global counter
    first_char_email = list(data[1])[0]
    chars = set('0123456789abcdefghijklmnopqrstuvwxyz')

    if first_char_email in chars:
        try:
            query_str = "insert into breach_compilation.\"{}\"(id, email, password, username, provider) VALUES (%s, %s, %s, %s, %s)".format(first_char_email)

            cursor.execute(query_str, data)
            db_conn.commit()
            counter += 1
            if (data[0] % 1000) == 0:
                trace_logger.info("inserted: " + str(data))
        except Exception as e:
            # save data which are not inserted
            error_logger.error(str(data))
            db_conn.commit()
    else:
        # handle symbols
        try:
            query_str = "insert into breach_compilation.symbols(id, email, password, username, provider) VALUES (%s, %s, %s, %s, %s)".format(first_char_email)

            cursor.execute(query_str, data)
            db_conn.commit()
            counter += 1
            if (counter % 1000) == 0:
                trace_logger.info("inserted: " + str(data))
        except Exception as e:
            # save data which are not inserted
            error_logger.error(str(data))
            db_conn.commit()


def iterate_data_dir(breach_compilation_path):

    # check if path includes data directory
    if 'data' not in os.listdir(breach_compilation_path):
        print("no 'data' directory in given BreachCompilation path")
        trace_logger.info("no 'data' directory in given BreachCompilation path")
        return
    # change to data path within breach compilation collection
    breach_compilation_path_data = os.path.join(breach_compilation_path, 'data')

    # iterate over all directories and differentiate between files and folder
    for root_dir in sorted(os.listdir(breach_compilation_path_data)):
        root_dir_abs = os.path.join(breach_compilation_path_data, root_dir)  # absolute path

        # check if it is a directory
        if os.path.isdir(root_dir_abs):
            for subdir in sorted(os.listdir(root_dir_abs)):
                subdir_abs = os.path.join(root_dir_abs, subdir)  # absolute path

                # check if it is a directory
                if os.path.isdir(subdir_abs):
                    for subsubdir in sorted(os.listdir(subdir_abs)):
                        subsubdir_abs = os.path.join(subdir_abs, subsubdir)  # absolute path

                        # check if it is a directory
                        if os.path.isdir(subsubdir_abs):
                            pass
                        else:
                            # handle files within folder
                            extract_data_file(subsubdir_abs)

                else:
                    # handle files within folder
                    extract_data_file(subdir_abs)
        else:
            # handle files within folder
            extract_data_file(root_dir_abs)


def extract_data_file(file_path):

    with open(file_path, mode='rb') as file:
        trace_logger.info("extract data from file " + str(file_path))
        # read all lines
        lines = file.readlines()
        try:
            for line in lines:
                cred_list = line.decode('utf-8').rstrip('\n').split(':')

                if len(cred_list) == 2:
                    handle_credentials(cred_list[0], cred_list[1])
                else:
                    error_logger.error("cred_list: " + str(cred_list))
        except UnicodeDecodeError as e:
            for line in lines:
                cred_list = line.decode('latin-1').rstrip('\n').split(':')

                if len(cred_list) == 2:
                    handle_credentials(cred_list[0], cred_list[1])
                else:
                    error_logger.error("cred_list: " + str(cred_list))


def handle_credentials(email, password):

    divide_email = email.split('@')

    if len(divide_email) == 2:
        username = divide_email[0]
        provider = divide_email[1]
        data = (counter, str(email), str(password), str(username), str(provider))
        if (counter % 50000) == 0:
            print(data)
        insert_data_in_db(data=data)
    else:
        error_logger.error("divide_email: " + str(divide_email))


def main():
    print("start script breachcompilation_to_postgresql.py")

    # arguments
    parser = argparse.ArgumentParser(description="script to insert BreachCompilation credentials into postgresql database")
    parser.add_argument('--host', type=str, help='')
    parser.add_argument('--port', type=str, help='')
    parser.add_argument('--user', type=str, help='')
    parser.add_argument('--password', type=str, help='')
    parser.add_argument('--dbname', type=str, help='')
    parser.add_argument('--path', type=str, help='')

    args = parser.parse_args()

    formate_logger()

    if (args.host and args.port and args.user and args.password and args.dbname and args.path) is None:
        print("Please specify all arguments")
        exit(1)
    else:
        # connecting to database
        connect_db(args.host, args.port, args.user, args.password, args.dbname)
        # check and create schema as well as all tables in database
        create_table()
        # iterate through the data directory structure and extract all credentials from each file
        iterate_data_dir(args.path)


if __name__ == '__main__':
    main()
