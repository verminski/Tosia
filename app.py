from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_owner = db.Column(db.Integer)
    name = db.Column(db.String(80), nullable=False)
    race = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    visits = db.relationship('Visit', backref='pet', lazy=True)

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    visits = relationship('Visit', backref='clinic', lazy=True)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    visit_time = db.Column(db.DateTime, nullable=False)
    problem = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addpet', methods=['GET', 'POST'])
def addpet():
    if request.method == 'POST':
        name = request.form['name']
        race = request.form['race']
        age = request.form['age']
        new_pet = Pet(name=name, race=race, age=age, is_active=True)
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/addpet')
    else:
        pets = Pet.query.filter_by(is_active=True).all()
        return render_template('addpet.html', pets=pets)

@app.route('/confirmdelete', methods=['POST'])
def confirmdelete():
    pet_id = request.form['pet_id']
    pet_to_delete = Pet.query.get_or_404(pet_id)
    if not pet_to_delete.is_active:
        return "Error, Pet not found", 404
    return render_template('confirm_delete.html', pet=pet_to_delete)

@app.route('/deletepet', methods=['POST'])
def deletepet():
    pet_id = request.form['pet_id']
    pet_to_delete = Pet.query.get_or_404(pet_id)
    if not pet_to_delete.is_active:
        return "Error, Pet not found", 404
    pet_to_delete.is_active = False
    db.session.commit()
    return redirect('/addpet')

@app.route('/bookvisit', methods=['GET', 'POST'])
def bookvisit():
    if request.method == 'POST':
        pet_id = request.form['pet_id']
        pet = Pet.query.get_or_404(pet_id)
        if not pet.is_active:
            return "Error, Pet not found", 404
        clinic_id = request.form['clinic_id']
        visit_time_str = request.form['visit_time']
        problem = request.form['problem']
        visit_time = datetime.strptime(visit_time_str, '%Y-%m-%dT%H:%M')
        new_visit = Visit(pet_id=pet_id, clinic_id=clinic_id, visit_time=visit_time, problem=problem)
        db.session.add(new_visit)
        db.session.commit()
        clinic = Clinic.query.get_or_404(clinic_id)
        return render_template('confirmation.html', pet=pet, clinic=clinic, visit_time=visit_time)
    else:
        pets = Pet.query.filter_by(is_active=True).all()
        clinics = Clinic.query.all()
        cat_image_url = get_random_cat_image()
        return render_template('bookvisit.html', pets=pets, clinics=clinics, cat_image_url=cat_image_url)

@app.route('/visithistory')
def visithistory():
    visits = Visit.query.join(Pet).filter(Pet.is_active==True).all()
    return render_template('visithistory.html', visits=visits)
def get_random_cat_image():
    response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=gif')
    data = response.json()
    return data[0]['url']

def create_dummy_clinics():
    clinics = Clinic.query.all()
    if len(clinics) == 0:
        clinic_names = ["Pazur", "ReksioVet", "Smętarz dla zwierząt", "Bark Bark Bitch", "Normalna Klinika Weterynaryjna"]
        for name in clinic_names:
            new_clinic = Clinic(name=name)
            db.session.add(new_clinic)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_dummy_clinics()
    app.run(debug=True)