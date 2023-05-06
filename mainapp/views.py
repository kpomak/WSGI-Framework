from config.generic import render
from mainapp.core import Engine, Logger

engine = Engine()
logger = Logger()

class TemplateView:
    template_name = "index.html"

    def __call__(self, request):
        return "200 OK", render(self.template_name, context=request)


class IndexView(TemplateView):
    pass


class AboutView(TemplateView):
    template_name = "about.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"

    def __call__(self, request):
        if request["method"] == "POST":
            message = request["params"]
            print(message)
        return super().__call__(request)

class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':

            data = request['params']

            name = data['name']
            name = engine.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = engine.find_category_by_id(int(category_id))

            new_category = engine.create_category(name, category)

            engine.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=engine.categories)
        else:
            categories = engine.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)
