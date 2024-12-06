from flask import Flask, jsonify, request
from flask_restx import Api, Resource, reqparse
from config import Config
from models import db, Terms, Vendors
from sqlalchemy import exc

app = Flask(__name__)
config = Config()
app.config.from_object(config)
db.init_app(app)

# API Setup
api = Api(app, version='1.0', title='Vendors API', description='Vendors Management API')
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

if __name__ == '__main__':
    app.run(debug=True)