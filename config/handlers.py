from config.utils import parse_request_params


class GetHandler:
    @staticmethod
    def get_params(env):
        query_string = env["QUERY_STRING"]
        return parse_request_params(query_string)


class PostHandler:
    @staticmethod
    def get_request_params(env):
        try:
            content_length = int(env.get("CONTENT_LENGTH"))
        except TypeError:
            content_length = 0

        return env["wsgi.input"].read(content_length) if content_length > 0 else b""

    def parse_data(self, data):
        result = {}
        if data:
            result = parse_request_params(data.decode("utf-8"))
        return result

    def get_params(self, environ):
        data = self.get_request_params(environ)
        return self.parse_data(data)


params_handler = {
    "GET": GetHandler,
    "POST": PostHandler,
}
