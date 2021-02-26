from flask import Flask, make_response, render_template, send_file, request
import pdfkit
from pyplot_handler import chart
from influx_handler_rg import dbase
import json
import time
from tz_correction import tz_correction as tz
from matplotlib import pyplot as plt, dates as mpl_dates

app = Flask(__name__)


@app.route('/sensor/<sensor>')
def sensor_image(sensor):
    return send_file(sensor_objs[sensor].retrieve_plot_dir())


# http://host/api?title=fishpond monitoring&from=${__from:date}&to=${__to:date}
@app.route('/api')
def api():
    utc_frm = request.args.get('from')
    utc_to = request.args.get('to')
    title = request.args.get('title')
    # time_string_sensor_lists = []

    frm = tz_corrector.get_string(utc_frm)
    to = tz_corrector.get_string(utc_to)
    variables = {
        'page-size': 'A4',
        'margin-top': '2cm',
        'margin-right': '2cm',
        'margin-bottom': '2cm',
        'margin-left': '2cm',
        'footer-right': '[page]',
        'frm': frm,
        'to': to,
        'title': title,
        'sensors': sensors,
        'host': reporter_host,
        'for_table': {}
    }

    for key in sensors:
        sensor_objs[key].generate_plot(utc_frm, utc_to)
        variables['for_table'][key] = sensor_objs[key].generate_table()

    time.sleep(2)
    # embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    rendered = render_template('report.html', variables=variables)
    options = {'enable-local-file-access': None}
    # css = "/home/ubuntu/project-study/report-generator/static/styles/stylesheet.css"
    # pdf = pdfkit.from_string(rendered, False, options=options, css=css)

    pdf = pdfkit.from_string(rendered, False, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
    # return rendered


if __name__ == "__main__":

    with open('/home/ubuntu/project-study/report-generator/config.json', 'r') as file:
        data = json.loads(file.read())
    sensors = {"ph": "pH", "tb": "turbidity",
               "temp": "temperature", "do": "dissolved oxygen"}
    sensor_objs = {}

    tz_corrector = tz(data['cloud']['timezone'])

    for key in sensors:
        sensor_objs[key] = chart(
            key, dbase(tz_corrector, key, data['cloud']['database'],
                       data['cloud']['username'], data['cloud']['password'],
                       data['cloud']['influxHost']), plt, mpl_dates)
    reporter_host = data['cloud']['grafana']
    app.run(host='0.0.0.0')
