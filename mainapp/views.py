from config.generic import render


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
