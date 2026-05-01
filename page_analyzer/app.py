from urllib.error import HTTPError

from flask import (
	Flask,
	render_template,
	request,
	flash,
	redirect,
	url_for,
	get_flashed_messages
)

from flask_bootstrap import Bootstrap5
from page_analyzer.repository import AnalyzerRepo
import validators
import os
from dotenv import load_dotenv
import requests


app = Flask(__name__)
bootstrap = Bootstrap5(app)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
repo = AnalyzerRepo()

@app.route('/')
def index():
	return render_template('index.html', url={}, errors={})

@app.route("/", methods=["POST"])
def add_url():
	url_to_check = request.form.get("url").strip()
	if not url_to_check:
		errors = {"name": "please enter url"}
		flash("Please enter url", 'danger')
		return render_template('index.html', url={"name": url_to_check}, errors=errors), 400
	if not validators.url(url_to_check):
		errors = {"name": "invalid url"}
		flash('Url is incorrect', 'danger')
		return render_template('index.html', url={"name": url_to_check}, errors=errors), 422
	try:
		url_id = repo.add_url_if_not_exists(url_to_check)
		return redirect(url_for('show_url_info', id=url_id))
	except Exception as e:
		flash(f'Ошибка при добавлении URL: {str(e)}', 'danger')
		return render_template('index.html', url={"name": url_to_check}, errors={}), 500


@app.route('/urls/<int:id>')
def show_url_info(id):
	info = repo.get_url_info(id)
	result = repo.get_results_by_id(id)
	if info is None:
		flash('Url is not found', 'danger')
		return render_template('index.html', url={}, errors={})
	if result is None:
		return render_template('url_info.html', info=info, result=[])
	return render_template('url_info.html', info=info, result=result)


@app.route('/urls')
def show_all_urls():
	urls = repo.get_urls()
	return render_template('all_urls.html', urls=urls)


@app.route('/urls/<id>/checks', methods=["POST"])
def check_id(id):
	try:
		url_name = repo.get_url_by_id(id)
		response = requests.get(url_name)
		response.raise_for_status()
		sc = response.status_code
	except HTTPError as e:
		flash(f'Error {e} occured while getting status code', 'danger')
		return redirect(url_for('show_url_info', id=id))
	if repo.do_check(id, sc) is True:
		flash('Successfully checked', 'success')
		return redirect(url_for('show_url_info', id=id))
	else:
		flash('Error occured while checking', 'danger')
		return redirect(url_for('show_url_info', id=id))




	


if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		port=8000,
		debug=True
	)
