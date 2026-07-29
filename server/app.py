from flask import request, jsonify, make_response
from flask_restful import Resource
from marshmallow import ValidationError
from config import app, db, api, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models import User, Note, UserSchema, NoteSchema
from datetime import date

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
        return UserSchema().dump(user), 200

class Notes(Resource):
    @jwt_required()
    def get(self, id=None):
        user_id = int(get_jwt_identity())
       
        if id is None:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 5, type=int)

            pagination = Note.query.filter(Note.user_id == user_id).order_by(Note.id).paginate(page=page, per_page=per_page, error_out=False)
            notes = pagination.items

            return {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "total_pages": pagination.pages,
                "items": NoteSchema().dump(notes, many=True)

            }, 200

        specific_note = Note.query.filter(
                Note.user_id == user_id,
                Note.id == id
            ).first()

        if not specific_note:
            return {"error": "Item not found"}, 404
        
        return NoteSchema().dump(specific_note), 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())

        data = request.get_json()
        title, content = data.get('title', None), data.get('content', None)

        if title is None:
            return {"error": "Enter a title"}, 400

        try:
            validated = NoteSchema().load({"title": title, "content": content, "created_at": date.today()})

        except ValidationError as err:
            return {"error_description": f"{err.messages}"}, 422

        new_note = Note(**validated, user_id=user_id)

        db.session.add(new_note)
        db.session.commit()

        return NoteSchema().dump(new_note), 201
        
    def put(self, id):
        user_id = int(get_jwt_identity())

        specific_note = Note.query.filter(
                Note.user_id == user_id,
                Note.id == id
            ).first()

        data = request.get_json()

        if not data:
            return {"error": "Invalid or missing JSON body"}, 400

        try:
            validated = NoteSchema().load(data)
        except ValidationError as err:
            return {"error_description": f"{err.messages}"}, 422

        specific_note.title = validated['title']
        specific_note.content = validated.get('content', None)

        db.session.commit()

        return NoteSchema().dump(specific_note), 200
        
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