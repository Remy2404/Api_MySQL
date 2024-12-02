from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Terms(db.Model):
    __tablename__ = "terms"
    terms_id = db.Column(db.Integer, primary_key=True)
    terms_description = db.Column(db.String(50), nullable=False)
    terms_due_days = db.Column(db.Integer, nullable=False)

class invoices(db.Model):
    __tablename__ = "invoices"
    invoice_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, nullable=False)
    invoice_number = db.Column(db.String(50), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    invoice_total = db.Column(db.Numeric(9, 2), nullable=False)
    payment_total = db.Column(db.Numeric(9, 2), nullable=False)
    credit_total = db.Column(db.Numeric(9, 2), nullable=False)
    terms_id = db.Column(db.Integer, db.ForeignKey("terms.terms_id"), nullable=False)
    invoice_due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date, nullable=True)  
    