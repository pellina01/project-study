from flask import Flask, make_response, render_template
import pdfkit

app = Flask(__name__)

@app.route('/<name>')
def main(name):
    rendered = render_template('hello-world.html',name=name) #embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response

if __name__ == "__main__":
    app.run()
