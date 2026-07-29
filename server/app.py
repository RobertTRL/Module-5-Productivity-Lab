from flask import request, jsonify, make_response
from flask_restful import Resource
from marshmallow import ValidationError
from config import app, db, api, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
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
        data = request.get_json()
        username, password = data.get('username', None), data.get('password', None)

        if username is None:
            return {"error": "Enter a username"}, 400
                
        if password is None:
            return {"error": "Enter a password"}, 400

        user = User.query.filter(User.username == username).first()

        if not user:
            return {'error': 'Unauthorized'}, 401

        if not user.authenticate(password):
            return {'error': 'Unauthorized'}, 401

        token = create_access_token(identity=str(user.id))

        return make_response(jsonify(token=token, user=UserSchema().dump(user)), 200)
        
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username, password, password_confirmation = data.get('username', None), data.get('password', None), data.get('password_confirmation', None)
        
        if username is None:
            return {"error": "Enter a username"}, 400
        
        if password is None or password_confirmation is None:
            return {"error": "Enter a password"}, 400

        if password != password_confirmation:
            return {"error": "Password and password confirmation do not match"}, 404

        try:
            new_user = User(username=username)
            
        except ValueError as err:
            return {"error": str(err)}, 422

        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=str(new_user.id))
        return make_response(jsonify(token=token, user=UserSchema().dump(new_user)), 201)  

class Identity(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(int(get_jwt_identity()))

        if not user:
            return {'error': 'Unauthorized'}, 401

        return UserSchema().dump(user), 200

class Notes(Resource):
    @jwt_required()
    def get(self, id=None):
        if id is None:
            pass

        pass

    def post(self):
        pass

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass    

api.add_resource(Login, '/login', endpoints='login')
api.add_resource(Signup, '/signup', endpoints='signup')
api.add_resource(Identity, '/me', endpoints='me')
api.add_resource(Notes, '/notes', '/notes/<int:id>', endpoints='notes')

if __name__ == '__main__':
    app.run(port=5555, debug=True)