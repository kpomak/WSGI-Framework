from http import HTTPStatus

from config.generic import render
from config.utils import route, debug
from config.views import engine, logger, TemplateView, ListView, CreateView
from mainapp.serializers import CourseSerializer
from mainapp.middleware import EmailNotifier, SmsNotifier


email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


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
            logger.log(request["params"])
        return super().__call__(request)


@route("/categories/create/")
class CreateCategoryView(CreateView):
    template_name = "create_category.html"

    @debug
    def create_instanse(self, data):
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


@route("/categories/")
class CategoryListView(ListView):
    template_name = "category_list.html"


@route("/courses/create/")
class CreateCourseView(CreateView):
    template_name = "create_course.html"

    @debug
    def create_instanse(self, data):
        category = engine.find_category_by_id(
            int(data.get("category_id")), engine.state["categories"]
        )
        try:
            course = engine.create_course(category=category, **data)
        except Exception:
            return f"{HTTPStatus.BAD_REQUEST} BAD REQUEST", render("index.html")
        else:
            course.observers.extend((email_notifier, sms_notifier))


@route("/courses/")
class CoursesListView(ListView):
    template_name = "courses_list.html"


@route("/courses/copy/")
class CopyCourseView(ListView):
    template_name = "courses_list.html"

    @debug
    def __call__(self, request):
        data = request["params"]
        name = data.get("name")
        course = engine.get_course(engine.state["categories"], name)
        course.clone()
        return super().__call__(request)


@route("/auth/register/")
class RegisterView(CreateView):
    template_name = "register.html"

    @debug
    def create_instanse(self, data):
        username = data.get("username")
        if username:
            engine.create_user(
                username,
                data.get("email"),
                data.get("phone"),
            )


@route("/students/")
class CoursesListView(ListView):
    template_name = "students_list.html"


@route("/students/subscribe/")
class SubscribeView(CreateView):
    template_name = "subscribe_course.html"

    @debug
    def create_instanse(self, data):
        course_name = data.get("course")
        student_id = data.get("student_id")
        if course_name and student_id:
            course = engine.get_course(engine.state["categories"], course_name)
            student = engine.state["users"][int(student_id)]
            if student not in course.students:
                course.add_student(student)

    @debug
    def __call__(self, request):
        if request["method"] == "POST":
            data = self.get_request_data(request)
            self.create_instanse(data)
            logger.log(f'request {request["method"]} create instanse from {data}')
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
