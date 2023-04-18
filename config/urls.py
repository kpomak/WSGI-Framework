from datetime import date
from mainapp.views import Index, About, Contacts


def today(context):
    context['date'] = date.today()


def hello_world(context):
    context['hello_world'] = 'Hello world!'


context_gen = (today, hello_world)

url_patterns = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
}