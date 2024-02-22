#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    response = [bakery.to_dict() for bakery in bakeries]
    return jsonify(response)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id = id).first()

    if bakery:
        response = bakery.to_dict()
        status_code = 200
    else:
        response = {"message": "Patient not found"}
        status_code = 404
    return make_response(response, status_code)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    bakeries = BakedGood.query.order_by(BakedGood.price.desc()).all()
    resp = [item.to_dict() for item in bakeries]
    return jsonify(resp)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_item = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not most_expensive_item:
        return jsonify({'error': 'No baked goods found'}), 404
    return jsonify(most_expensive_item.to_dict())


if __name__ == '__main__':
    app.run(port=5555, debug=True)
