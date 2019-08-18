import psycopg2


class PostgresqlHandler:

    def __init__(self, host, port, user, password, dbname):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

        self.connection = None
        self.cursor = self.__connect()

    def __del__(self):
        """ destructor

        """
        if self.connection is not None:
            self.connection.close()

    def close(self):
        """ closes the postgresql connection cleanly

        """
        if self.connection is not None:
            self.connection.close()

    def __connect(self):
        """

        :return:
        """
        try:

            self.connection = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password, dbname=self.dbname)
            return self.connection.cursor()

        except Exception as e:
            print(e)
            exit(1)

    def execute_query(self, query_str):
        """

        :return:
        """
        self.cursor.execute(query_str)

    def commit_query(self):
        """

        :return:
        """
        self.connection.commit()


    def create_table(self):
        """

        :return:
        """
        query_str = "create table breach_compilation.test (id integer, num integer)"
        self.execute_query(query_str)
        self.commit_query()
        print("test")


if __name__ == '__main__':
    db = PostgresqlHandler(host="192.168.178.37", port="5432", user="christian", password="", dbname="hacking")
    db.create_table()