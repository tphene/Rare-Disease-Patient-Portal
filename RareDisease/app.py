from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rare_disease.db'
db = SQLAlchemy(app)

### Models for database tables
class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(120), unique=True)
    disease_desc = db.Column(db.Text)
    disease_desc_new = db.Column(db.Text)
    disease_desc_old = db.Column(db.Text)
    disease_links = db.Column(db.Text)
    def __init__(self,disease_name):
        self.disease_name = disease_name
    def __rept__(self):
        return '<Disease %r>' % self.disease_name

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_name = db.Column(db.String(120), unique=True)
    therapy_desc = db.Column(db.Text)
    cost_per_session = db.Column(db.Float(6,2))
    def __init__(self,therapist_name):
        self.therapist_name = therapist_name
    def __rept__(self):
        return '<Therapist %r>' % self.therapist_name

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(120), unique=True)
    medicine_desc = db.Column(db.Text)
    cost_per_unit = db.Column(db.Float(6,2))
    def __init__(self,medicine_name):
        self.medicine_name = medicine_name
    def __rept__(self):
        return '<Medicine %r>' % self.medicine_name

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), unique=True)
    therapy_cost_factor = db.Column(db.Float(2  ,2), nullable=False)
    medicine_cost_factor = db.Column(db.Float(2, 2), nullable=False)
    therapy_cost_factor1 = db.Column(db.Float(2, 2), nullable=False)
    medicine_cost_factor1 = db.Column(db.Float(2, 2), nullable=False)
    therapy_cost_factor2 = db.Column(db.Float(2, 2), nullable=False)
    medicine_cost_factor2 = db.Column(db.Float(2, 2), nullable=False)
    therapy_cost_factor3 = db.Column(db.Float(2, 2), nullable=False)
    medicine_cost_factor3 = db.Column(db.Float(2, 2), nullable=False)
    def __init__(self,location_name):
        self.location_name = location_name
    def __rept__(self):
        return '<Location %r>' % self.location_name

class Medicine_req(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    m_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    m_req = db.Column(db.Integer, nullable=False)
    m_req1 = db.Column(db.Integer, nullable=False)
    m_req2 = db.Column(db.Integer, nullable=False)
    m_req3 = db.Column(db.Integer, nullable=False)
    medicine_req_desc = db.Column(db.Text)

class Therapist_req(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    d_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    t_id = db.Column(db.Integer, db.ForeignKey('therapist.id'), nullable=False)
    t_req = db.Column(db.Integer, nullable=False)
    t_req1 = db.Column(db.Integer, nullable=False)
    t_req2 = db.Column(db.Integer, nullable=False)
    t_req3 = db.Column(db.Integer, nullable=False)
    therapy_req_desc = db.Column(db.Text)


### For index page
@app.route('/')
def index():
    diseases = Disease.query.all()
    return render_template("index.html", disease=diseases)

### For query page
@app.route('/query', methods=['POST'])
def query():
    location = Location.query.all()
    stage = request.form['stage']
    disease = request.form['diagnosis']
    diseaseObj = Disease.query.filter(Disease.disease_name == disease).first()
    links = diseaseObj.disease_links
    print(diseaseObj.disease_name)
    if stage == 'Newly Diagnosed':
        desciption = diseaseObj.disease_desc_new
        stage = 'new'
    else:
        desciption = diseaseObj.disease_desc_old
        stage = 'old'
    return render_template("query.html",state = location, disease=disease, stage=stage, desc = desciption, links=links)

### For result page
@app.route('/result',methods=['POST'])
def result():
    ### Getting data from query form
    name=request.form['name']
    age = request.form['age']
    state = request.form['option']
    salary = request.form['salary']
    stage = request.form['stage']
    disease = request.form['disease']
    locationObj = Location.query.filter(Location.location_name == state).first()

    ### Getting cost factors from locations table

    ### Annual
    tcf = (locationObj.therapy_cost_factor)
    mcf = (locationObj.medicine_cost_factor)

    ### Year2
    tcf1 = (locationObj.therapy_cost_factor1)
    mcf1 = (locationObj.medicine_cost_factor1)
    ### Year3
    tcf2 = (locationObj.therapy_cost_factor2)
    mcf2 = (locationObj.medicine_cost_factor2)
    ### Year4
    tcf3 = (locationObj.therapy_cost_factor3)
    mcf3 = (locationObj.medicine_cost_factor3)

    ### Get medicine and therapy requirements for the disease selected
    disease_id = Disease.query.filter(Disease.disease_name == disease).first().id

    medicine_req = Medicine_req.query.filter(Medicine_req.d_id == disease_id).all()
    medicines = []
    medicine_units_annual = []
    medicine_units_year1 = []
    medicine_units_year2 = []
    medicine_units_year3 = []
    medicine_desc = []
    therapy_desc = []

    for medicine in medicine_req:
        medicine_units_annual.append(medicine.m_req)
        medicine_units_year1.append(medicine.m_req1)
        medicine_units_year2.append(medicine.m_req2)
        medicine_units_year3.append(medicine.m_req3)
        medicines.append(Medicine.query.filter(Medicine.id == medicine.m_id).first())
        medicine_desc.append(medicine.medicine_req_desc)

    therapy_req = Therapist_req.query.filter(Therapist_req.d_id == disease_id).all()
    therapies = []
    therapy_sessions_annual = []
    therapy_sessions_year1 = []
    therapy_sessions_year2 = []
    therapy_sessions_year3 = []
    for therapy in therapy_req:
        therapist = Therapist.query.filter(Therapist.id == therapy.t_id).first()
        if therapist.therapist_name == 'Pediatrician' and int(age) > 18:
            continue
        therapy_sessions_annual.append(therapy.t_req)
        therapy_sessions_year1.append(therapy.t_req1)
        therapy_sessions_year2.append(therapy.t_req2)
        therapy_sessions_year3.append(therapy.t_req3)
        therapies.append(therapist)
        therapy_desc.append(therapy.therapy_req_desc)

    ### Get the cost for medicine and therapy for the disease
    annual_medicine_cost = 0
    year1_medicine_cost = 0
    year2_medicine_cost = 0
    year3_medicine_cost = 0
    annual_therapy_cost = 0
    year1_therapy_cost = 0
    year2_therapy_cost = 0
    year3_therapy_cost = 0
    for i in range(len(medicines)):
        unit_cost = medicines[i].cost_per_unit
        annual_medicine_cost += unit_cost * mcf * medicine_units_annual[i]
        year1_medicine_cost += unit_cost * mcf1 * medicine_units_year1[i]
        year2_medicine_cost += unit_cost * mcf2 * medicine_units_year2[i]
        year3_medicine_cost += unit_cost * mcf3 * medicine_units_year3[i]

    hours_for_therapy = 0
    for i in range(len(therapies)):
        session_cost = therapies[i].cost_per_session
        hours_for_therapy += therapy_sessions_annual[i]
        annual_therapy_cost += session_cost * tcf * therapy_sessions_annual[i]
        year1_therapy_cost += session_cost * tcf1 * therapy_sessions_year1[i]
        year2_therapy_cost += session_cost * tcf2 * therapy_sessions_year2[i]
        year3_therapy_cost += session_cost * tcf3 * therapy_sessions_year3[i]

    ### Data for prediction chart
    therapy_cost_pred=[int(year1_therapy_cost),int(year2_therapy_cost),int(year3_therapy_cost)]
    medicine_cost_pred = [int(year1_medicine_cost), int(year2_medicine_cost), int(year3_medicine_cost)]

    ###Lost opportunity
    lost_opportunity = int(int(salary) / 2080 * hours_for_therapy)

    return render_template('result.html', disease = disease, therapies = therapies, medicines = medicines, medicine_data_annual=[int(annual_medicine_cost)], medicine_data_pred=medicine_cost_pred,
                           therapy_data_annual=[int(annual_therapy_cost)],therapy_data_pred=therapy_cost_pred,
                           hours_for_therapy=hours_for_therapy,salary=salary,lost_opportunity=lost_opportunity, medicine_desc=enumerate(medicine_desc), therapy_desc=enumerate(therapy_desc),
                           medicine_desc_comp=enumerate(medicine_desc), therapy_desc_comp=enumerate(therapy_desc))

if(__name__ == "__main__"):
    app.run(debug=True)

