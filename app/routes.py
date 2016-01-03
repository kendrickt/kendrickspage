from flask import render_template
from app import app
from .forms import TestForm
from testapp import add


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/projects/<projectname>')
def specific_projects(projectname):
    return render_template('projects/%s.html' % projectname)


@app.route("/test", methods=['GET', 'POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        return str(add.add_2_ints(form.int_a.data, form.int_b.data))
    return render_template('test.html', form=form)
