from flask import Flask, request, jsonify
from models import db, Terms , Invoices
from sqlalchemy import exc

app = Flask(__name__)

# Configure the MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ramy2404@localhost:3306/ap'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Endpoint to retrieve all terms (detailed version)
@app.get('/terms')
def get_terms():
    terms_query = db.session.query(Terms).with_entities(Terms.terms_id, Terms.terms_description, Terms.terms_due_days)
    terms_list = []
    for term in terms_query:
        terms_list.append({
            "id": term.terms_id,
            "description": term.terms_description,
            "due_days": term.terms_due_days
        })
    return jsonify(terms_list)


# POST method to add a new term
@app.post('/terms')
def post_terms():
    try:
        request_data = request.get_json()
        t = Terms(
            terms_description=request_data["terms_description"], 
            terms_due_days=request_data["terms_due_days"]
        )
        db.session.add(t)
        db.session.commit()
        return {'message':'success'}, 201
    except Exception as e:
        print(e)
        return {'message': 'Something went wrong!'}, 500

# PUT method to update term information
@app.put('/terms/<string:des>')
def put_terms(des):
    request_data = request.get_json()
    t = db.session.query(Terms).filter(Terms.terms_description == des).first()
    if t:
        t.terms_description = request_data["terms_description"]
        t.terms_due_days = request_data["terms_due_days"]
        try:
            db.session.commit()
            return {'message':'Success'}
        except exc.SQLAlchemyError as e:
            return {'message': str(e.__cause__)}
    else:
        return {'message':'There is no record'},400

# DELETE method to remove a term record
@app.delete('/terms/<int:id>')
def delete_terms(id):
    t = db.session.query(Terms).filter(Terms.terms_id == id).first()
    if t:
        db.session.delete(t)
        try:
            db.session.commit()
            return {'message':'Success'}
        except exc.SQLAlchemyError as e:
            return {'message': str(e.__cause__)}
    else:
        return {'message':'There is no record'},400

@app.get('/invoices')
def get_invoices():
    invoices_query = db.session.query(Invoices).with_entities(Invoices.invoice_id, Invoices.vendor_id, Invoices.invoice_number, Invoices.invoice_date, Invoices.invoice_total, Invoices.payment_total, Invoices.credit_total, Invoices.terms_id, Invoices.invoice_due_date, Invoices.payment_date)
    invoices_list = []
    for invoice in invoices_query:
        invoices_list.append({
            "id": invoice.invoice_id,
            "vendor_id": invoice.vendor_id,
            "invoice_number": invoice.invoice_number,
            "invoice_date": invoice.invoice_date,
            "invoice_total": invoice.invoice_total,
            "payment_total": invoice.payment_total,
            "credit_total": invoice.credit_total,
            "terms_id": invoice.terms_id,
            "invoice_due_date": invoice.invoice_due_date,
            "payment_date": invoice.payment_date
        })
    return invoices_list
#GET method to retrieve invoices by term id
@app.get('/Invoices/term/<int:term_id>')
def get_invoices_term(term_id):
    inv = db.session.query(Invoices, Terms)\
        .join(Terms, Terms.terms_id == Invoices.terms_id)\
        .with_entities(Invoices.invoice_number, Terms.terms_description)\
        .filter(Invoices.terms_id == term_id).all()
    lst = [v._asdict() for v in inv]
    return lst

# Run the application
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
