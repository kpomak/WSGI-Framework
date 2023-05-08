from datetime import date

import mainapp.views as mainapp


def today(context):
    context["date"] = date.today()


def hello_world(context):
    context["hello_world"] = "Hello world!"


context_gen = (today, hello_world)

url_patterns = {
    "/": mainapp.IndexView(),
    "/about/": mainapp.AboutView(),
    "/contacts/": mainapp.ContactsView(),
    "/courses/": mainapp.CoursesListView(),
    "/courses/create/": mainapp.CreateCourseView(),
    "/courses/copy/": mainapp.CopyCourseView(),
    "/categories/": mainapp.CategoryListView(),
    "/categories/create/": mainapp.CreateCategoryView(),
}
