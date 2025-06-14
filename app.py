import os

import jinja2 as jinja

from chalice import Chalice, Response # type: ignore
                                      # Even though Pylance flags a private import error
                                      # The Chalice docs suggest this import line


app = Chalice(app_name='steady_grewp')


@app.route('/')
def index():
    env = jinja.Environment(
        loader=jinja.FileSystemLoader("templates")
    )
    template = env.get_template('article.html')
    return Response(
        body=template.render(article_name='article_name'),
        status_code=200,
        headers={'Content-Type': 'text/html'}
    )

@app.route('/img/logo.png')
def logo():
    file_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'logo.png')
    with open(file_path, 'rb') as logo_file:
        return Response(
            body=logo_file.read(),
            status_code=200,
            headers={'Content-Type': 'image/png'}
        )
