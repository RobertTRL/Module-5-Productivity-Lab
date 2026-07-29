from flask import request, jsonify, make_response
from flask_restful import Resource
from marshmallow import ValidationError
from config import app, db, api, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from models import User, Note, UserSchema, NoteSchema

"""
Tested endpoints:
    -> POST /login
    -> POST /signup
    -> GET /me

Other endpoints(not tested):
    -> GET /notes
    -> GET /notes/<int:id>
    -> POST /notes
    -> PUT /notes/<int:id>
    -> PATCH /notes/<int:id>
    -> DELETE /notes/<int:id>

"""

class Login(Resource):
    def post(self):
        username, password = request.get('username', None), request.get('password', None)

        if username is None:
            return {"error": "Enter a username"}, 404
                
        if password is None:
            return {"error": "Enter a password"}, 404

        user = User.query.filter(User.username == username).first()

        if not user:
            return {'error': 'Unauthorized'}, 401

        if not user.authenticate(password):
            return {'error': 'Unauthorized'}, 401

        token = create_access_token(identity=str(user.id))

        return make_response(jsonify(token=token, user=UserSchema().dump(user)), 200)
        
class Signup(Resource):
    def post(self):
        username, password, password_confirmation = request.get('username', None), request.get('password', None), request.get('password_confirmation', None)
        
        if username is None:
            return {"error": "Enter a username"}, 404
        
        if password or password_confirmation is None:
            return {"error": "Enter a password"}, 404

        if password != password_confirmation:
            return {"error": "Password and password confirmation do not match"}, 404

        try:
            UserSchema().load({"username": username})

        except ValidationError as err:
            return jsonify({"error_description": f"{err.messages}"}), 400

        new_user = User(username=username)
        new_user.password_hash = password
        token = create_access_token(identity=str(new_user.id))

        db.session.add()
        db.session.commit() 

        return make_response(jsonify(token=token, user=UserSchema().dump(new_user)), 200)   

class Identity(Resource):
    pass

api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Identity, '/me', endpoint='me')

if __name__ == '__main__':
    app.run(port=5555, debug=True)