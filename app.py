efrom flask import Flask, render_template, request, redirect, url_for, flashfrom flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



app.secret_key = "your-secret-key"  # Palitan mo ng mas secure na string

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sample user
users = {"testuser": {"password": "testpass"}}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
@login_required
def home():
    return f"Hello, {current_user.id}! You are logged in."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
    return '''
    <form method="POST">
      Username: <input type="text" name="username"/><br/>
      Password: <input type="password" name="password"/><br/>
      <input type="submit" value="Login"/>
    </form>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged out!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
