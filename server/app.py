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

if __name__ == '__main__':
    app.run(port=5555, debug=True)