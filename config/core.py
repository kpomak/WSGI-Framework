from config.handlers import params_handler


class PageNotFound404:
    def __call__(self, request):
        return "404 NOT FOUND", f"404 page not found"


class Rainbow:
    def __init__(self, urls, controllers):
        self.urls = urls
        self.controllers = controllers

    def __call__(self, environ, start_response):
        request = {}

        path = environ["PATH_INFO"]

        method = environ["REQUEST_METHOD"]
        request["method"] = method

        request["params"] = params_handler[method]().get_params(environ)

        if not path.endswith("/"):
            path = f"{path}/"

        if path in self.urls:
            view = self.urls[path]
        else:
            view = PageNotFound404()

        for controller in self.controllers:
            controller(request)

        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])
        return [body.encode("utf-8")]
