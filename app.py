from flask import Flask, render_template, request, redirect, url_for, jsonify
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Dummy user data (you can replace this with a database)
users = {}

# User class for Flask-Login
class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user = User()
        user.id = user_id
        return user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/secured')
@login_required
def secured():
    return render_template('secured.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]):
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('secured'))
    else:
        return render_template('index.html', error='Invalid username or password')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users[username] = hashed_password
    return render_template('index.html', success='Registration successful!')

# Simulated Bitcoin data (replace with actual implementation)
bitcoin_balance = 13.1890
bitcoin_price = 5453858.86 # Removed the commas for float conversion

# Route to serve the secured page
@app.route('/secure_page')
def secure_page():
    return render_template('secured_page.html')

# Route to provide Bitcoin data
@app.route('/bitcoin_data')
def bitcoin_data():
    return jsonify({'balance': bitcoin_balance, 'price': bitcoin_price})

if __name__ == '__main__':
    app.run(debug=True)
