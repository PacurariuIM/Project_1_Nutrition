import requests

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import IngredientForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Debugging table
@app.route('/db_check')
def db_check():
    with app.app_context():
        tables = db.engine.table_names()
        return f"Tables in database: {tables}"
    
# Route to get ingredients, send request, return recipes
SPOONACULAR_API_KEY='9b9efdf863ff4457a17b867b0962413b'
@app.route('/get_recipes', methods=['GET', 'POST'])
@login_required
def get_recipes():
    form = IngredientForm()
    recipes = None
    if form.validate_on_submit():
        # Get ingredients from the form
        ingredients = form.ingredients.data
        # Make a request to Spoonacular API
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=10&apiKey={SPOONACULAR_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            recipes = response.json()  # List of recipes returned by the API
        else:
            flash('Failed to fetch recipes. Please try again.', 'danger')
    
    return render_template('get_recipes.html', form=form, recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)