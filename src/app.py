from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Terms , invoices

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
    return terms_list

# Endpoint to retrieve all terms (short version using list comprehension)
@app.get('/terms1')
def get_terms1():
    terms_query = db.session.query(Terms).with_entities(Terms.terms_id, Terms.terms_description, Terms.terms_due_days)
    return [term._asdict() for term in terms_query]

@app.get('/invoices')
def get_invoices():
    invoices_query = db.session.query(invoices).with_entities(invoices.invoice_id, invoices.vendor_id, invoices.invoice_number, invoices.invoice_date, invoices.invoice_total, invoices.payment_total, invoices.credit_total, invoices.terms_id, invoices.invoice_due_date, invoices.payment_date)
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
# Run the application
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
