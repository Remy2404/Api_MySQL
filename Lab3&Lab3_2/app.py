from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Terms, Invoices, Vendors
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ramy2404@localhost:3306/ap'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# GET method for retrieving specific terms
@app.get('/terms/<int:id>')
def get_term(id):
    t = db.session.query(Terms)\
        .with_entities(Terms.terms_id, Terms.terms_description, Terms.terms_due_days)\
        .filter(Terms.terms_id == id).first()
    if t:
        return jsonify(t._asdict())
    return jsonify({'message': 'Term not found'}), 404

# GET method to retrieve all invoices with specific terms
@app.get('/invoices/term/<int:term_id>')
def get_invoices_term(term_id):
    inv = db.session.query(Invoices, Terms)\
        .join(Terms, Terms.terms_id == Invoices.terms_id)\
        .with_entities(Invoices.invoice_number, Terms.terms_description)\
        .filter(Invoices.terms_id == term_id).all()
    lst = [v._asdict() for v in inv]
    return jsonify(lst)

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
        return jsonify({'message':'success'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong!'}), 500

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
            return jsonify({'message':'Success'})
        except exc.SQLAlchemyError as e:
            return jsonify({'message': str(e.__cause__)})
    else:
        return jsonify({'message':'There is no record'}), 400

# DELETE method to remove a term record
@app.delete('/terms/<int:id>')
def delete_terms(id):
    t = db.session.query(Terms).filter(Terms.terms_id == id).first()
    if t:
        db.session.delete(t)
        try:
            db.session.commit()
            return jsonify({'message':'Success'})
        except exc.SQLAlchemyError as e:
            return jsonify({'message': str(e.__cause__)})
    else:
        return jsonify({'message':'There is no record'}), 400

# GET method to retrieve all vendors
@app.get('/vendors')
def get_vendors():
    vendors = db.session.query(Vendors).all()
    vendor_list = []
    for vendor in vendors:
        vendor_dict = {
            'vendor_id': vendor.vendor_id,
            'vendor_name': vendor.vendor_name,
            'vendor_address1': vendor.vendor_address1,
            'vendor_address2': vendor.vendor_address2,
            'vendor_city': vendor.vendor_city,
            'vendor_state': vendor.vendor_state,
            'vendor_zip_code': vendor.vendor_zip_code,
            'vendor_phone': vendor.vendor_phone,
            'vendor_contact_last_name': vendor.vendor_contact_last_name,
            'vendor_contact_first_name': vendor.vendor_contact_first_name,
            'default_terms_id': vendor.default_terms_id,
            'default_account_number': vendor.default_account_number
        }
        vendor_list.append(vendor_dict)
    return jsonify(vendor_list)

# POST method to add a new vendor
@app.post('/vendors')
def post_vendor():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 415
    try:
        request_data = request.get_json()
        vendor = Vendors(
            vendor_name=request_data['vendor_name'],
            vendor_address1=request_data['vendor_address1'],
            vendor_address2=request_data.get('vendor_address2'),  # Optional
            vendor_city=request_data['vendor_city'],
            vendor_state=request_data['vendor_state'],
            vendor_zip_code=request_data['vendor_zip_code'],
            vendor_phone=request_data.get('vendor_phone'),  # Optional
            vendor_contact_last_name=request_data.get('vendor_contact_last_name'),  # Optional
            vendor_contact_first_name=request_data.get('vendor_contact_first_name'),  # Optional
            default_terms_id=request_data['default_terms_id'],
            default_account_number=request_data['default_account_number']
        )
        db.session.add(vendor)
        db.session.commit()
        return jsonify({'message': 'Vendor added successfully'}), 201
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.__cause__)}), 500

@app.put('/vendors/<int:vendor_id>')
def update_vendor(vendor_id):
    try:
        request_data = request.get_json()
        vendor = db.session.query(Vendors).get(vendor_id)
        if vendor:
            vendor.vendor_name = request_data['vendor_name']
            vendor.vendor_address1 = request_data['vendor_address1']
            vendor.vendor_address2 = request_data.get('vendor_address2')
            vendor.vendor_city = request_data['vendor_city']
            vendor.vendor_state = request_data['vendor_state']
            vendor.vendor_zip_code = request_data['vendor_zip_code']
            vendor.vendor_phone = request_data.get('vendor_phone')
            vendor.vendor_contact_last_name = request_data.get('vendor_contact_last_name')
            vendor.vendor_contact_first_name = request_data.get('vendor_contact_first_name')
            vendor.default_terms_id = request_data['default_terms_id']
            vendor.default_account_number = request_data['default_account_number']
            db.session.commit()
            return jsonify({'message': 'Vendor updated successfully'})
        else:
            return jsonify({'message': 'Vendor not found'}), 404
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.__cause__)}), 500
@app.delete('/vendors/<int:vendor_id>')

def delete_vendor(vendor_id):
    vendor = db.session.query(Vendors).get(vendor_id)
    if vendor:
        db.session.delete(vendor)
        db.session.commit()
        return jsonify({'message': 'Vendor deleted successfully'})
    else:
        return jsonify({'message': 'Vendor not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)