from config.generic import render
from mainapp.engine import Engine, Logger
from http import HTTPStatus

engine = Engine()
logger = Logger(f"{__name__}")

class TemplateView:
    template_name = "index.html"

    def __call__(self, request):
        request['state'] = engine.state
        logger.log(f'request {request["method"]} {self.template_name}')
        return f"{HTTPStatus.OK}", render(self.template_name, context=request)


class IndexView(TemplateView):
    pass


class AboutView(TemplateView):
    template_name = "about.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"

    def __call__(self, request):
        if request["method"] == "POST":
            message = request["params"]
            logger.log(message)
        return super().__call__(request)

class CreateCategory(TemplateView):
    template_name = 'create_category.html'
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['params']
            name = data.get('name')
            if name:
                engine.create_category(name)
            logger.log(f'request {request["method"]} create category {data}')
            return f"{HTTPStatus.CREATED}", render('index.html', context=request)
        else:
            return super().__call__(request)

class CategoryList(TemplateView):
    template_name = 'category_list.html'

    
class CreateCourse(TemplateView):
    template_name = 'create_course.html'
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['params']
            category = engine.find_category_by_id(int(data.get('category_id')))
            try:
                engine.create_course(category=category, **data)
            except Exception:
                pass
            request['state'] = engine.state
            logger.log(f'request {request["method"]} create course {data}')
            return f'{HTTPStatus.CREATED}', render('courses_list.html', context=request)

        else:
            super().__call__(request)
        
class CoursesList(TemplateView):
    template_name = "courses_list.html"

class CopyCourse:
    template_name = "courses_list.html"
    def __call__(self, request):
        data = request['params']
        name = data.get('name')
        course = engine.get_course(name)
        course.clone()
        super().__call__(request)


