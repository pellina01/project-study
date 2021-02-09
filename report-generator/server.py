from flask import Flask, make_response, render_template, send_file
import pdfkit
from matplotlib import pyplot as plt 

app = Flask(__name__)

def plot():
    x = [1,2,3] 
    y = [2,4,1] 
    # plotting the points  
    plt.plot(x, y) 
    # naming the x axis 
    plt.xlabel('x - axis') 
    # naming the y axis 
    plt.ylabel('y - axis') 
    # giving a title to my graph 
    plt.title('My first graph!') 
    # function to show the plot 
    plt.savefig('images/chart1.png')

@app.route('/images/chart1')
def psample():
    return send_file('images/chart1.png')


@app.route('/<name>')
def main(name):
    plot()
    rendered = render_template('report.html',name=name) #embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
    # return rendered

@app.route('/api/<fromm>/<to>')
def api(fromm, to):
    return "from:{fromm} to:{to}".format(fromm=fromm, to=to)


if __name__ == "__main__":
    app.run(host= '0.0.0.0')
