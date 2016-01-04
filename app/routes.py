from flask import render_template, jsonify, request, redirect, url_for
from app import app
from .forms import TestForm
from testapp import add as add2ints
from homefieldadvantage import app as generate_plot


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    return redirect(url_for('specific_projects', projectname='no_project'))


@app.route('/projects/<projectname>')
def specific_projects(projectname):
    return render_template('projects/%s.html' % projectname)


@app.route('/test', methods=['GET', 'POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        return str(add2ints.add_2_ints(form.int_a.data, form.int_b.data))
    return render_template('test.html', form=form)


@app.route('/add', methods=['POST'])
def add():
    return jsonify({
        'sum': str(
            add2ints.add_2_ints(
                int(request.form['a']),
                int(request.form['b'])
            )
        )
    })


@app.route('/makeplot_20160103', methods=['POST'])
def makeplot_20160103():
    return jsonify({
        'result': generate_plot.run(
            'temp',
            request.form['startyear'],
            request.form['endyear'],
            request.form['xaxis'],
            request.form['yaxis']
        )
    })
