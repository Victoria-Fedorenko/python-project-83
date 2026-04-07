from flask import (
	Flask,
	render_template,
	request,
	flash,
	redirect,
	url_for
)

from flask_bootstrap import Bootstrap5
from page_analyzer.repository import AnalyzerRepo
import psycopg2
import validators
import os
from dotenv import load_dotenv


app = Flask(__name__)
bootstrap = Bootstrap5(app)

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
conn = psycopg2.connect(DATABASE_URL,
    sslmode='require',
    connect_timeout=10,
    keepalives=1,
    keepalives_idle=5,
    keepalives_interval=2,
    keepalives_count=3
)
repo = AnalyzerRepo(conn)

@app.route('/')
def index():
	return render_template('index.html', url={}, errors={})

@app.route("/", methods=["POST"])
def add_url():
	url_to_check = request.form.get("url")
	if not url_to_check:
		errors = {"name": "please enter url"}
		flash("Please enter url", 'danger')
		return render_template('/', url={"name": url_to_check}, errors=errors)
	if not validators.url(url_to_check):
		errors = {"name": "invalid url"}
		flash('Url is incorrect', 'danger')
		return render_template('/', url={"name": url_to_check}, errors=errors)
	try:
		url_id = repo.add_url_if_not_exists(url_to_check)
		return redirect(url_for('show_url_info', id=url_id))
	except Exception as e:
		flash(f'Ошибка при добавлении URL: {str(e)}', 'danger')
		return render_template('index.html', url={"name": url_to_check}, errors={}), 500


@app.route('/urls/<int:id>')
def show_url_info(id):
	info = repo.get_url_info(id)
	if info is None:
		flash('Url is not found', 'danger')
		return redirect('/', url={}, errors={})
	return render_template('url_info.html', info=info)
	



if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		port=8000,
		debug=True
	)
