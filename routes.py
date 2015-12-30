from flask import Flask, render_template

app = Flask(__name__)


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


@app.route("/test")
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
