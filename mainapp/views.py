from http import HTTPStatus

from config.generic import render
from config.utils import Logger, route, debug
from mainapp.engine import Engine
from mainapp.serializers import CourseSerializer
from mainapp.middleware import EmailNotifier, SmsNotifier

engine = Engine()
logger = Logger(f"{__name__}")
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


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

    @debug
    def __call__(self, request):
        if request["method"] == "POST":
            message = request["params"]
            logger.log(message)
        return super().__call__(request)


@route("/categories/create/")
class CreateCategoryView(TemplateView):
    template_name = "create_category.html"

    @debug
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["params"]
            name = data.get("name")
            category_id = data.get("category_id")
            if category_id:
                category_id = int(category_id)
                category = engine.find_category_by_id(
                    category_id, engine.state["categories"]
                )
            else:
                category = None
            if name:
                engine.create_category(name, category)
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

    @debug
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["params"]
            category = engine.find_category_by_id(
                int(data.get("category_id")), engine.state["categories"]
            )
            try:
                course = engine.create_course(category=category, **data)
            except Exception:
                return f"{HTTPStatus.BAD_REQUEST} BAD REQUEST", render(
                    "courses_list.html", context=request
                )
            else:
                course.observers.extend((email_notifier, sms_notifier))
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

    @debug
    def __call__(self, request):
        data = request["params"]
        name = data.get("name")
        course = engine.get_course(engine.state["categories"], name)
        course.clone()
        return super().__call__(request)


@route("/auth/register/")
class RegisterView(TemplateView):
    template_name = "register.html"

    @debug
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["params"]
            username = data.get("username")
            if username:
                engine.create_user(
                    username,
                    data.get("email"),
                    data.get("phone"),
                )
                return f"{HTTPStatus.CREATED} CREATED", render(
                    "index.html", context=request
                )
        return super().__call__(request)


@route("/students/")
class CoursesListView(TemplateView):
    template_name = "students_list.html"


@route("/students/subscribe/")
class SubscribeView(TemplateView):
    template_name = "subscribe_course.html"

    def __call__(self, request):
        if request["method"] == "POST":
            data = request["params"]
            course_name = data.get("course")
            student_id = data.get("student_id")
            if course_name and student_id:
                course = engine.get_course(engine.state["categories"], course_name)
                student = engine.state["users"][int(student_id)]
                if student not in course.students:
                    course.add_student(student)
            return f"{HTTPStatus.CREATED} CREATED", render(
                "index.html", context=request
            )
        request["courses"] = engine.get_courses(engine.state["categories"])
        return super().__call__(request)


@route("/api/courses/")
class CourseViewSet:
    def __call__(self, request):
        return (
            "200 OK",
            CourseSerializer(engine.get_courses(engine.state["categories"])).save(),
        )
