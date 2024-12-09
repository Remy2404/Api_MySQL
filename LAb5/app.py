from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse , fields
from config import Config
from models import db, Terms, Vendors , Gender 
from sqlalchemy import exc

app = Flask(__name__)
config = Config()
app.config.from_object(config)
db.init_app(app)

# Single API Setup
api = Api(app, version='1.0', title='API Management System', description='API for Terms, Vendors and Gender Management')
api_ns = api.namespace("Reference", path='/apiv1', description="Reference Data")

# Parsers
put_terms_parser = reqparse.RequestParser()
put_terms_parser.add_argument('terms_description', type=str, required=True, help='Terms description is required')
put_terms_parser.add_argument('terms_due_days', type=int, required=True, help='Terms due days is required')

vendor_parser = reqparse.RequestParser()
vendor_parser.add_argument('vendor_name', type=str, required=True)
vendor_parser.add_argument('vendor_address1', type=str)
vendor_parser.add_argument('vendor_address2', type=str)
vendor_parser.add_argument('vendor_city', type=str, required=True)
vendor_parser.add_argument('vendor_state', type=str, required=True)
vendor_parser.add_argument('vendor_zip_code', type=str, required=True)
vendor_parser.add_argument('vendor_phone', type=str)
vendor_parser.add_argument('vendor_contact_last_name', type=str)
vendor_parser.add_argument('vendor_contact_first_name', type=str)
vendor_parser.add_argument('default_terms_id', type=int, required=True)
vendor_parser.add_argument('default_account_number', type=int, required=True)

@api_ns.route('/terms/<int:id>')
class TermResource(Resource):
    @api.doc('get_term')
    def get(self, id):
        term = Terms.query.get(id)
        if term:
            return {'terms_id': term.terms_id,
                   'terms_description': term.terms_description,
                   'terms_due_days': term.terms_due_days}
        return {'message': 'Term not found'}, 404

    @api.doc('update_term')
    @api.expect(put_terms_parser)
    def put(self, id):
        args = put_terms_parser.parse_args()
        term = Terms.query.get(id)
        if term:
            term.terms_description = args['terms_description']
            term.terms_due_days = args['terms_due_days']
            db.session.commit()
            return {'message': 'Term updated successfully'}
        return {'message': 'Term not found'}, 404

@api_ns.route('/vendors')
class VendorsResource(Resource):
    @api.doc('list_vendors')
    def get(self):
        vendors = Vendors.query.all()
        return {'vendors': [{'vendor_id': v.vendor_id, 'vendor_name': v.vendor_name} for v in vendors]}

    @api.doc('create_vendor')
    @api.expect(vendor_parser)
    def post(self):
        args = vendor_parser.parse_args()
        try:
            vendor = Vendors(**args)
            db.session.add(vendor)
            db.session.commit()
            return {'message': 'Vendor created successfully'}, 201
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e.__cause__)}, 500

@api_ns.route('/vendors/<int:vendor_id>')
class VendorResource(Resource):
    @api.doc('update_vendor')
    @api.expect(vendor_parser)
    def put(self, vendor_id):
        vendor = Vendors.query.get(vendor_id)
        if not vendor:
            return {'message': 'Vendor not found'}, 404
        
        args = vendor_parser.parse_args()
        try:
            for key, value in args.items():
                setattr(vendor, key, value)
            db.session.commit()
            return {'message': 'Vendor updated successfully'}
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            return {'error': str(e.__cause__)}, 500

    @api.doc('delete_vendor')
    def delete(self, vendor_id):
        vendor = Vendors.query.get(vendor_id)
        if vendor:
            db.session.delete(vendor)
            db.session.commit()
            return {'message': 'Vendor deleted successfully'}
        return {'message': 'Vendor not found'}, 404

#Gender API Models
# Gender API Models
gender_fields = api.model('Gender', {
    'id': fields.Integer(description='The unique identifier'),
    'name_latin': fields.String(description='The Latin name'),
    'acronym': fields.String(description='The acronym')
})

#Gender parser
gender_parser = reqparse.RequestParser()
gender_parser.add_argument('name_latin', type=str, required=True, help='Name Latin is required')
gender_parser.add_argument('acronym', type=str, required=True, help='Acronym is required')
@api_ns.route('/gender')
class GenderListResource(Resource):
    @api.marshal_list_with(gender_fields)
    def get(self):
        """List all genders"""
        genders = Gender.query.all()
        return genders

    @api.expect(gender_parser)
    @api.marshal_with(gender_fields)
    def post(self):
        """Create a new gender"""
        args = gender_parser.parse_args()
        new_gender = Gender(
            name_latin=args['name_latin'],
            acronym=args['acronym']
        )
        try:
            db.session.add(new_gender)
            db.session.commit()
            return new_gender, 201
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            api.abort(500, str(e.__cause__))

@api_ns.route('/gender/<int:id>')
class GenderResource(Resource):
    @api.marshal_with(gender_fields)
    def get(self, id):
        """Get a gender by ID"""
        gender = Gender.query.get(id)
        if gender:
            return gender
        api.abort(404, "Gender not found")

    @api.expect(gender_parser)
    @api.marshal_with(gender_fields)
    def put(self, id):
        """Update a gender"""
        gender = Gender.query.get(id)
        if not gender:
            api.abort(404, "Gender not found")
            
        args = gender_parser.parse_args()
        try:
            gender.name_latin = args['name_latin']
            gender.acronym = args['acronym']
            db.session.commit()
            return gender
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            api.abort(500, str(e.__cause__))

    @api.response(204, 'Gender deleted')
    def delete(self, id):
        """Delete a gender"""
        gender = Gender.query.get(id)
        if not gender:
            api.abort(404, "Gender not found")
            
        try:
            db.session.delete(gender)
            db.session.commit()
            return '', 204
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            api.abort(500, str(e.__cause__))
if __name__ == '__main__':
    app.run(debug=True)