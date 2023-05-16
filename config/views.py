from http import HTTPStatus

from config.utils import Logger
from config.generic import render
from mainapp.engine import Engine

logger = Logger("server")
engine = Engine()


class TemplateView:
    template_name = "index.html"

    def get_context(self, request):
        pass

    def render_template(self, request):
        logger.log(f'request {request["method"]} {self.template_name}')
        self.get_context(request)
        return f"{HTTPStatus.OK} OK", render(self.template_name, context=request)

    def __call__(self, request):
        return self.render_template(request)


class ListView(TemplateView):
    queryset = engine.state
    context_name = "state"

    def get_queryset(self):
        return self.queryset

    def get_context(self, request):
        request[self.context_name] = self.get_queryset()


class CreateView(ListView):
    @staticmethod
    def get_request_data(request):
        return request["params"]

    def create_instanse(self, data):
        pass

    def __call__(self, request):
        if request["method"] == "POST":
            data = self.get_request_data(request)
            self.create_instanse(data)
            logger.log(f'request {request["method"]} create instanse from {data}')
            return self.render_template(request)
        else:
            return super().__call__(request)
