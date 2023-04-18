from jinja2 import Template
from os.path import join
from os import getcwd


def render(template_name, folder='templates', **kwargs):

    file_path = join(getcwd(), folder, template_name)

    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)