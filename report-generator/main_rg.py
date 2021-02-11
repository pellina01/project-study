from flask import Flask, make_response, render_template, send_file
import pdfkit
import chart_dbquery_handler

app = Flask(__name__)


@app.route('/sensor/<sensor>')
def psample(sensor):
    return send_file('images/{}.png'.format(sensor))


@app.route('/api/<frm>/<to>/<title>')
def api(frm, to, title):
    sensor_to_render = []
    for sensor in sensors:
        pass
        plot( [1,2,3], [2,4,1], sensor)
        sensor_to_render.append(sensor)

    rendered = render_template('report.html',title=title, sensors=sensor_to_render) #embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    options = {'enable-local-file-access': None}
    css = "report-generator/templates/stylesheet.css"
    pdf = pdfkit.from_string(rendered, False, options=options, css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    sensor_to_render = []
    return response
    # return rendered

if __name__ == "__main__":
    sensors = ["ph", "tb", "temp", "do"]
    app.run(host= '0.0.0.0')
