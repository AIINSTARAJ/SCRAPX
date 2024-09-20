from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder="templates")
app.config['SECRET_KEY'] = 'r4W/@ygh899AAA776Y3Z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.Text(20),nullable = False)


    def __repr__(self):
        return f'<Data {self.username}>'

@app.route('/')
def index():
    return redirect(url_for('login'))   

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = Data.query.filter_by(username=username).first()
        if existing_user:
            flash('!Username already exists. Please choose a different one.')
            return redirect(url_for('signup'))
        new_user = Data(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        User = Data.query.filter_by(username=username).first()
        if User and User.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard',username = User.username))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    data = Data.query.filter_by(username = username).first()
    return render_template("dashboard.html", data = data)

if __name__ == '__main__':
    app.run(debug=False, host= '127.25.115.0', port = 8080)



