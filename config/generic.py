# from jinja2 import Template
# from os.path import join
# from os import getcwd


# def render(template_name, folder='templates', **kwargs):

#     file_path = join(getcwd(), folder, template_name)

#     with open(file_path, encoding='utf-8') as f:
#         template = Template(f.read())
#     return template.render(**kwargs)



from jinja2 import Environment, PackageLoader, select_autoescape

def render(template_name, folder='templates', **kwargs):
    env = Environment(
        loader=PackageLoader("mainapp"),
        autoescape=select_autoescape()
    )
    template = env.get_template(template_name)


    return template.render(**kwargs)

