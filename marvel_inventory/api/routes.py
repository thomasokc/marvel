# a route is what makes the 'folder in a folder' system work and allow us to create unique sub-domain names or URL's that can be accessed from the front end

from flask import Blueprint, jsonify,request
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, User, Hero,hero_schema,heros_schema

api = Blueprint('api',__name__,url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return {'some':'value'}


# Create Hero
@api.route('/heros', methods=['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_created = request.json['date_created']
    user_token = current_user_token.token

    hero = Hero(name,description,comics_appeared_in,super_power,date_created,user_token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

#pick a hero
@api.route('/heros/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token):
    owner = current_user_token.token
    hero = Hero.query.get(id)
    response = heros_schema.dump(hero)
    return jsonify(response)

#delete
@api.route('/heros/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)