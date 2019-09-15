from flask import Response, request


class APIHandler:

    def __init__(self):
        pass

    def get_passwords(self):
        """

        :param email:
        :return:
        """
        email = request.headers.get('email')
        print(email)
        # db interface
        res = Response(status=200)
        res.data = "password: abc"
        return res
