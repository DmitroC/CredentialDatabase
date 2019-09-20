import json
from flask import Response, request
from BreachCompilationRestAPI.db.fetcher import DBFetcher


class APIHandler:
    """ class APIHandler to link routes to specific handler function

    USAGE:
            api = APIHandler(host=host, port=port, username=username, password=password, dbname=dbname)
            api.get_passwords()
    """
    def __init__(self, host, port, username, password, dbname):

        self.db = DBFetcher()
        try:
            self.db.connect(host=host, port=port, username=username, password=password, dbname=dbname, minConn=1, maxConn=5)
        except Exception as e:
            print(e)

    def index(self):
        """

        :return:
        """
        return "hello world"

    def get_passwords(self):
        """ gets specific email from request header

        :return: json string with a list of passwords dedicated to requested email
        """
        email = request.headers.get('email')
        if '@' in email:
            first_letter = email[0].lower()
            sql = "select password from test.\"{}\" where email='{}'".format(first_letter, email)
            result = self.db.all(sql=sql, autocommit=True)

            pass_list = list()
            for entry in result:
                pass_list.append(entry[0])
            #print(pass_list)
            pass_dict = {'passwords': pass_list}

            return Response(response=json.dumps(pass_dict), status=200, mimetype='application/json')
        else:
            return Response(response="no valid email address", status=400)

    def get_sha1(self):
        """

        :return:
        """
        password = request.headers.get('password')

        if isinstance(password, str):
            # query every table, if sha1 string was found break current query
            pass
        else:
            return Response(response="no valid password string provided", status=400)

    def get_sha256(self):
        """

        :return:
        """
        pass

    def get_sha512(self):
        """

        :return:
        """
        pass

    def get_md5(self):
        """

        :return:
        """
        pass
