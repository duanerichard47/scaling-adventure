#!/usr/bin/env python3

from flask import Flask,  make_response, jsonify,request
from flask_migrate import Migrate

from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Home Page'

@app.route('/vendors', methods=['GET'])
def vendors():
    if request.method == 'GET':
        vendors = []
        for vendor in Vendor.query.all():
            vendor_dict = vendor.to_dict()
            vendors.append(vendor_dict)

        response = make_response(
            jsonify(vendors),
            200
        )

        return response


@app.route('/vendors/<int:id>')
def vendor_by_id(id):
    
    vendor = Vendor.query.filter(Vendor.id == id).first()
    if vendor == None:
        response_body = {
            "error": "Vendor not found"
        }
        response = make_response(jsonify(response_body), 404)

        return response

    elif request.method == 'GET':
            vendor = Vendor.query.filter(Vendor.id == id).first()
            vendor_dict = vendor.to_dict()

            response = make_response(
                jsonify(vendor_dict),
                200
            )

            return response
  

@app.route('/sweets')
def sweets():
    if request.method == 'GET':
        sweets = []
        for sweet in Sweet.query.all():
            sweet_dict = sweet.to_dict()
            sweets.append(sweet_dict)

        response = make_response(
            jsonify(sweets),
            200
        )

        return response
    

@app.route('/sweets/<int:id>')
def sweet_by_id(id):

    sweet = Sweet.query.filter(Sweet.id == id).first()

    if sweet == None:
        response_body = {
             "error": "Sweet not found"
        }
        response = make_response(jsonify(response_body), 404)

        return response

    elif request.method == 'GET':
            sweet_dict = sweet.to_dict()

            response = make_response(
                jsonify(sweet_dict),
                200
            )

            return response
   

@app.route('/vendor_sweets', methods=['GET', 'POST'])
def vendor_sweets():

    if request.method == 'GET':
        vendor_sweets = []
        for vendor_sweet in VendorSweet.query.all():
            vendor_sweet_dict = vendor_sweet.to_dict()
            vendor_sweets.append(vendor_sweet_dict)

        response = make_response(
            jsonify(vendor_sweets),
            200
        )

        return response
    
    elif request.method == 'POST':
        new_vendor_sweet = VendorSweet(
            price=request.json.get("price"),
            vendor_id=request.json.get("vendor_id"),
            sweet_id=request.json.get("sweet_id")
        )

        db.session.add(new_vendor_sweet)
        db.session.commit()

        vendor_sweet_dict = new_vendor_sweet.to_dict()

        response = make_response(
            jsonify(vendor_sweet_dict),
            201
        )

        return response
    
    

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def vendor_sweet_by_id(id):
    vendor_sweet = VendorSweet.query.filter(VendorSweet.id == id).first()

    if vendor_sweet == None:
        response_body = {
            "error": "VendorSweet not found"
        }
        response = make_response(jsonify(response_body), 404)

        return response
    
    elif request.method == 'DELETE': 
            db.session.delete(vendor_sweet)
            db.session.commit()

            response_body = {}

            response = make_response(
                jsonify(response_body),
                200
            )

            return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)

   
