# encoding: utf-8
# Created by woolf

import os
import logging
from flask import send_from_directory, make_response
import matplotlib.pyplot as plot
import io

from . import home

from flask import (
    render_template,
    request)
from flask.views import View

@home.route('/')
def index():
    # app.logger.debug('Debug test')
    return render_template('home/welcome.html')

# @home.route('/hello')
@home.route('/hello/<name>')
def hello_world(name = None):
    return render_template('home/hello.html', name=name)
    #return 'Hello, World!'

# yet another router
class MyView(View):
    methods = ['GET']

    def dispatch_request(self, name):
        return 'Hello %s!' % name

home.add_url_rule('/hello/<name>', view_func=MyView.as_view('myview'))

@home.route('/about')
def about():
    return 'The about page'

@home.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# below method just for test
@home.route('/user/<name>')
def show_user_profile(name):
    return 'User %s name' % name

@home.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@home.route('/image/<title>')
def images(title):
    return render_template("home/image.html", title=title)

@home.route('/fig/<title>')
def fig(title):
    # fig = draw_polygons(title)
    # img = StringIO()
    # fig.savefig(img)
    # img.seek(0)
    # return send_file(img, mimetype='image/png')
    import datetime
    from io import StringIO
    import random

    # create image
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)

    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))

    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    
    # set canvas
    canvas=FigureCanvas(fig)
    png_output = io.BytesIO()
    canvas.print_png(png_output)

    # output image to web stream
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response