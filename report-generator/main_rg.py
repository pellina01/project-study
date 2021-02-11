from flask import Flask, make_response, render_template, send_file
import pdfkit
from pyplot_handler import chart
from influx_handler_rg import dbase
import json

app = Flask(__name__)


@app.route('/sensor/<sensor>/<frm>/<to>')
def psample(sensor, frm, to):
    return send_file(sensor_objs[sensor].generate_plot(frm, to))


@app.route('/api/<frm>/<to>/<title>')
def api(frm, to, title):
    variables = {
    'frm ': frm,
    'to' : to,
    'title' : title,
    'sensors' : sensors
    }
    rendered = render_template('report.html', variables = variables ) #embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    options = {'enable-local-file-access': None}
    css = "report-generator/templates/stylesheet.css"
    pdf = pdfkit.from_string(rendered, False, options=options, css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
    # return rendered

if __name__ == "__main__":

    with open('/home/ubuntu/project-study/report-generator/config.json', 'r') as file:
        data = json.loads(file.read())
    sensors = ["ph", "tb", "temp", "do"]
    sensor_objs = {}

    for sensor in sensors:
        sensor_objs[sensor]=chart(
                sensor, dbase(sensor, data['cloud']['database'], 
                data['cloud']['username'], data['cloud']['password'], 
                data['cloud']['influxHost']))

    app.run(host= '0.0.0.0')
