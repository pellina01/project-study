from flask import Flask
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

app = Flask(__name__)

file_loader = FileSystemLoader(
    'C:/assorted-projects/thesis/flask-pdf/html-to-pdf/templates')
env = Environment(loader=file_loader)
template = env.get_template('hello-world.html')


@app.route('/')
def main():
    html_out = template.render(name='johny')
    return HTML(string=html_out).write_pdf()


if __name__ == "__main__":
    app.run()
