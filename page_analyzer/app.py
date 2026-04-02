from flask import (
	Flask,
	render_template,
	request,
	flash,
	redirect
)

from flask_bootstrap import Bootstrap5
from page_analyzer.repository import AnalyzerRepo
import psycopg2
import validators

app = Flask(__name__)
bootstrap = Bootstrap5(app)

conn = psycopg2.connect(DATABASE_URL)
repo = AnalyzerRepo(conn)

@app.route('/')
def index():
	return render_template('index.html', url={}, errors={})

@app.route("/", methods=["POST"])
def add_url():
	url_to_check = request.form.get("url")
	if not url_to_check:
		return "Url не указан", 400
	if not validators.url(url_to_check):
		errors = {"name": "invalid url"}
		flash('Url is incorrect')
		return redirect('/', url=url_to_check, errors=errors)
	repo.add_url(url_to_check)

@app.route('/urls/<id>')
def show_url_info(id):
	info = repo.get_url_info(id)
	return render_template('url_info.html', info=info)



if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		port=8000,
		debug=True
	)
