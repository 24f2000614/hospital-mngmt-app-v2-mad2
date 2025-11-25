from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Blacklist
from sqlalchemy.exc import IntegrityError

blacklist_field = {
    "email": fields.String
}


class Blacklist_Apis(Resource):
    def get(self):
        blacklist = Blacklist.query.all()
        return [marshal(blackItem, blacklist_field) for blackItem in blacklist]
