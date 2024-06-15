#Импорт
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import time


app = Flask(__name__)

# Connecting SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating a DB
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #email
    email = db.Column(db.String(30), nullable=False)
    #text
    text = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Feedback{self.id}>'
    

#Halaman Konten Berjalan
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        email = request.form['email']
        text = request.form['text']

        feed=Feedback(email = email, text = text)
        db.session.add(feed)
        db.session.commit()
        return redirect('/')

#Keterampilan Dinamis
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    button_discord = request.form.get('button_discord')
    button_html = request.form.get('button_html')
    button_db = request.form.get('button_db')
    return render_template('index.html', button_python=button_python,
                                         button_discord=button_discord,
                                         button_html=button_html,
                                         button_db=button_db)

if __name__ == "__main__":

    db_path = os.path.join(app.instance_path,'feedback.db')
    if not os.path.exists(db_path):
        print("Creating database......")
    time.sleep(2)
    with app.app_context():
        db.create_all()
    print("Database feedback.db has been successfully created :)")
    print("Location DB: ", app.instance_path)

    app.run(debug=True)
