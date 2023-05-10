from http import HTTPStatus

from config.generic import render
from config.utils import Logger, route
from mainapp.engine import Engine

engine = Engine()
logger = Logger(f"{__name__}")


class TemplateView:
    template_name = "index.html"

    def __call__(self, request):
        request["state"] = engine.state
        logger.log(f'request {request["method"]} {self.template_name}')
        return f"{HTTPStatus.OK} OK", render(self.template_name, context=request)


@route("/")
class IndexView(TemplateView):
    pass


@route("/about/")
class AboutView(TemplateView):
    template_name = "about.html"


@route("/contacts/")
class ContactsView(TemplateView):
    template_name = "contacts.html"

    def __call__(self, request):
        if request["method"] == "POST":
            message = request["params"]
            logger.log(message)
        return super().__call__(request)


@route("/categories/create/")
class CreateCategoryView(TemplateView):
    template_name = "create_category.html"

    def __call__(self, request):
        if request["method"] == "POST":
            data = request["params"]
            name = data.get("name")
            if name:
                engine.create_category(name)
            logger.log(f'request {request["method"]} create category {data}')
            return f"{HTTPStatus.CREATED} CREATED", render(
                "index.html", context=request
            )
        else:
            return super().__call__(request)


@route("/categories/")
class CategoryListView(TemplateView):
    template_name = "category_list.html"


@route("/courses/create/")
class CreateCourseView(TemplateView):
    template_name = "create_course.html"

    def __call__(self, request):
        if request["method"] == "POST":
            data = request["params"]
            category = engine.find_category_by_id(int(data.get("category_id")))
            try:
                engine.create_course(category=category, **data)
            except Exception:
                return f"{HTTPStatus.BAD_REQUEST} BAD REQUEST", render(
                    "courses_list.html", context=request
                )
            else:
                request["state"] = engine.state
                logger.log(f'request {request["method"]} create course {data}')
            return f"{HTTPStatus.CREATED} CREATED", render(
                "courses_list.html", context=request
            )
        else:
            return super().__call__(request)


@route("/courses/")
class CoursesListView(TemplateView):
    template_name = "courses_list.html"


@route("/courses/copy/")
class CopyCourseView(TemplateView):
    template_name = "courses_list.html"

    def __call__(self, request):
        data = request["params"]
        name = data.get("name")
        course = engine.get_course(name)
        course.clone()
        return super().__call__(request)
