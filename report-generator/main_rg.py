from flask import Flask, make_response, render_template, send_file, request
import pdfkit
from pyplot_handler import chart
from influx_handler_rg import dbase
import json
from tz_correction import tz_correction as tz

app = Flask(__name__)


@app.route('/sensor/<sensor>/<frm>/<to>')
def psample(sensor, frm, to):
    return send_file(sensor_objs[sensor].retrieve_plot_dir())


# @app.route('/api/<title>/<utc_frm>/<utc_to>')
# def api(title, utc_frm, utc_to):
# http://3.236.45.125:5000/api/fishpond/${__from:date:iso}/${__to:date:iso}

# http://hostname:5000/api?title=fishpond&from=${__from:date:iso}&to=${__to:date:iso}
@app.route('/api')
def api():
    utc_frm = request.args.get('from')
    utc_to = request.args.get('to')
    title = request.args.get('title')

    for sensor in sensors:
        sensor_objs[sensor].generate_plot(utc_frm, utc_to)

    frm = tz_corrector.set_to_ph(utc_frm)
    to = tz_corrector.set_to_ph(utc_to)
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

    tz_corrector = tz("Asia/Manila")

    for sensor in sensors:
        sensor_objs[sensor] = chart(
            sensor, dbase(tz_corrector, sensor, data['cloud']['database'],
                          data['cloud']['username'], data['cloud']['password'],
                          data['cloud']['influxHost']))

    app.run(host='0.0.0.0')
