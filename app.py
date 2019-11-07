from flask import Flask,  render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Windows2025*@localhost/library_feedback'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rddbekrevcawsv:8dea87d266bae9a240b9baa7d31dd47c236440582e1c3cf724ba6732b6a8890c@ec2-54-221-214-3.compute-1.amazonaws.com:5432/dfiv440auqorp4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    book = db.Column(db.String(200))
    publisher = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, book, publisher, rating, comments):
        self.customer = customer
        self.book = book 
        self.publisher = publisher
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        book = request.form['book']
        publisher = request.form['publisher']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer,book, publisher, rating, comments)
        if customer == '' or comments == '':
            return render_template('index.html', message = 'Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer and Feedback.book == book).count() == 0:
            data = Feedback(customer, book, publisher, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, book, publisher, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message = 'You have already submitted your feedback')




if __name__ == '__main__':
    app.run()
