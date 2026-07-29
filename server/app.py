from flask import request
from flask_restful import Resource

from config import app, db, api
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
    pass

class Signup(Resource):
    pass

class Identity(Resource):
    pass

api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Identity, '/me', endpoint='me')

if __name__ == '__main__':
    app.run(port=5555, debug=True)