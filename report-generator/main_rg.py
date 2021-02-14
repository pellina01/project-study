from flask import Flask, make_response, render_template, send_file, request
import pdfkit
from pyplot_handler import chart
from influx_handler_rg import dbase
import json
from datetime import datetime
from dateutil import tz

app = Flask(__name__)

def tz_correction(time_in_z):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Philippines/Manila')
    utc = datetime.strptime(time_in_z, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central

@app.route('/sensor/<sensor>/<frm>/<to>')
def psample(sensor, frm, to):
    return send_file(sensor_objs[sensor].retrieve_plot_dir())


@app.route('/api/<title>/<zfrm>/<zto>')
def api(title, zfrm, zto):
    frm = tz_correction(zfrm)
    to = tz_correction(zto)
    for sensor in sensors:
        sensor_objs[sensor].generate_plot(frm, to)

    variables = {
        'frm': frm,
        'to': to,
        'title': title,
        'sensors': sensors
    }
    # embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    rendered = render_template('report.html', variables=variables)
    options = {'enable-local-file-access': None}
    css = "/home/ubuntu/project-study/report-generator/templates/stylesheet.css"
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
        sensor_objs[sensor] = chart(
            sensor, dbase(sensor, data['cloud']['database'],
                          data['cloud']['username'], data['cloud']['password'],
                          data['cloud']['influxHost']))

    app.run(host='0.0.0.0')
