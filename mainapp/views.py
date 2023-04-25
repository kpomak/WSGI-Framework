from config.generic import render


class TemplateView:
    template_name = "index.html"

    def __call__(self, context):
        return '200 OK', render(self.template_name, context=context)


class IndexView(TemplateView):
    pass


class AboutView(TemplateView):
    template_name = "about.html"
    

class ContactsView(TemplateView):
    template_name = "contacts.html"



