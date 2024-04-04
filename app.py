from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import json
import analysis
import genre_analysis
from topairing import topAiring
import secrets
import MetrixChallenge

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.sqlite3'
app.secret_key = 'session404'  # Add this line
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)  # Yeh line add karo
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    api_key = db.Column(db.String(64))  # API key ke liye column add karo

    def __repr__(self):
        return f'<User {self.email}>'


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/doc')
def doc():
    return render_template('doc.html')

@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/ranking')
def ranking():
    json_data = analysis.top_1000()
    if json_data is not None:
        # Convert JSON string to Python list of dictionaries
        series_data = json.loads(json_data)
    else:
        # Agar json_data None hai, toh empty list assign kar do
        series_data = []
    return render_template('ranking.html', series=series_data)

@app.route('/allanime')
def allanime():
    json_data = analysis.all_Anime()
    if json_data is not None:
        # Convert JSON string to Python list of dictionaries
        series_data = json.loads(json_data)
    else:
        # Agar json_data None hai, toh empty list assign kar do
        series_data = []
    return render_template('allanime.html', series=series_data)

@app.route('/genre')
def genre():
    json_data = genre_analysis.genre()
    if json_data is not None:
        # Convert JSON string to Python list of dictionaries
        series_data = json.loads(json_data)
    else:
        # Agar json_data None hai, toh empty list assign kar do
        series_data = []
    return render_template('genre_list.html', series=series_data)

@app.route('/topairing')
def topairing():
    json_data = topAiring()
    if json_data is not None:
        # Convert JSON string to Python list of dictionaries
        series_data = json.loads(json_data)
    else:
        # Agar json_data None hai, toh empty list assign kar do
        series_data = []
    return render_template('topAiring.html', series=series_data)


@app.route('/generate_api')
def generate_api():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    if not user.api_key:
        user.api_key = secrets.token_hex(32)  # Generate a new API key if not present
        db.session.commit()

    return render_template('api_key.html', api_key=user.api_key)


@app.route('/generate_new_api_key', methods=['POST'])
def generate_new_api_key():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    user.api_key = secrets.token_hex(32)
    db.session.commit()

    return redirect(url_for('generate_api'))

@app.route('/api=<api_key>/allanime')
def all_anime_data(api_key):
    user = User.query.filter_by(api_key=api_key).first()  # Query the user with the provided API key
    if user:
        # Your code to fetch and return all anime data goes here
        data = analysis.all_Anime()
        return jsonify(json.loads(data))  # Ensure the data is returned in JSON format
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/totalanime')
def totalanime(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.total_anime()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/scoredata')
def scoredata(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.score_data()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/genre_count')
def genre_count(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.genre_count()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/episode_count')
def episode_count(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.total_eps_basedon_type()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/avg_fav')
def avg_fav(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.avg_type()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/anime_type')
def anime_type(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.count_anime_type()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/anime_by_rating')
def anime_by_rating(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    rating = request.args.get('rating')
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.anime_by_rating(rating)
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/anime_aired')
def anime_aired(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.anime_aired()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/top10_popular')
def top10_popular(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.top10_popular()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")

@app.route('/api=<api_key>/top20_favorite')
def top20_favorite(api_key):
    user = User.query.filter_by(api_key=api_key).first()
    if user:
        # Fetching Data from analysis file
        data = MetrixChallenge.top20_favorite()
        return jsonify(json.loads(data))
    else:
        abort(401, description="Invalid API Key")


# Operations functions:
@app.route('/perform_registration', methods=['POST'])
def perform_registration():
    name = request.form.get('user_ka_name')
    email = request.form.get('user_ka_email')
    password = request.form.get('user_ka_password')

    # User Input Validation
    if not name or not email or not password:
        return render_template('register.html', message='Please fill out all fields.')

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return render_template('register.html', message='Registration failed. Email already exists.')

    # Add new user
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return render_template('login.html', message='Registration successful. Kindly login to proceed.')


@app.route('/perform_login', methods=['POST'])  # Typo fixed here
def perform_login():
    email = request.form.get('user_ka_email')
    password = request.form.get('user_ka_password')
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session['user_id'] = user.id  # Store user ID in session
        return render_template('home.html', message='Login successful.')
    else:
        return render_template('login.html', message='Login failed! Please try again.')

if __name__ == '__main__':
    app.run(debug=True)