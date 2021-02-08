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
    plt.savefig('report-generator/templates/psample.png')

@app.route('/img/psample')
def psample():
    return send_file('templates/psample.png')


@app.route('/<name>')
def main(name):
    plot()
    rendered = render_template('hello-world.html',name=name) #embedded jinja2 on flask default directory is templates/ . there is no need to indicate to the path
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
    # return rendered

if __name__ == "__main__":
    app.run()
