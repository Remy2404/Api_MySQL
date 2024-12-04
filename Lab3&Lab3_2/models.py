from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Terms(db.Model):
    __tablename__ = "terms"
    terms_id = db.Column(db.Integer, primary_key=True)
    terms_description = db.Column(db.String(50), nullable=False)
    terms_due_days = db.Column(db.Integer, nullable=False)

class Vendors(db.Model):
    __tablename__ = "vendors"
    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(50), nullable=False, unique=True)
    vendor_address1 = db.Column(db.String(50), nullable=True)
    vendor_address2 = db.Column(db.String(50), nullable=True)
    vendor_city = db.Column(db.String(50), nullable=False)
    vendor_state = db.Column(db.String(2), nullable=False)
    vendor_zip_code = db.Column(db.String(20), nullable=False)
    vendor_phone = db.Column(db.String(50), nullable=True)
    vendor_contact_last_name = db.Column(db.String(50), nullable=True)
    vendor_contact_first_name = db.Column(db.String(50), nullable=True)
    default_terms_id = db.Column(db.Integer, db.ForeignKey("terms.terms_id"), nullable=False)
    default_account_number = db.Column(db.Integer, nullable=False)

class Invoices(db.Model):
    __tablename__ = "invoices"
    invoice_id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.vendor_id"), nullable=False)
    invoice_number = db.Column(db.String(50), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    invoice_total = db.Column(db.Numeric(9,2), nullable=False)
    payment_total = db.Column(db.Numeric(9,2), nullable=False, default=0)
    credit_total = db.Column(db.Numeric(9,2), nullable=False, default=0)
    terms_id = db.Column(db.Integer, db.ForeignKey("terms.terms_id"), nullable=False)
    invoice_due_date = db.Column(db.Date, nullable=False)
    payment_date = db.Column(db.Date, nullable=True)