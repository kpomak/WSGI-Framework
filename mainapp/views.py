from config.generic import render


class Index:
    def __call__(self, context):
        return '200 OK', render('index.html', context=context)


class About:
    def __call__(self, context):
        return '200 OK', render('about.html', context=context)
    
class Contacts:
    def __call__(self, context):
        return '200 OK', render('contacts.html', context=context)