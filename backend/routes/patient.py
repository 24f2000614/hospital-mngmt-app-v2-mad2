from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from api import 

patient_bp = Blueprint("patient", __name__)

