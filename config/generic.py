from jinja2 import Environment, PackageLoader, select_autoescape

def render(template_name, folder='templates', **kwargs):
    env = Environment(
        loader=PackageLoader("mainapp"),
        autoescape=select_autoescape()
    )
    template = env.get_template(template_name)


    return template.render(**kwargs)

