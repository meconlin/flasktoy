import flask
from flask import jsonify
import flask.ext.sqlalchemy
import flask.ext.restless
from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from flask.ext.restful import reqparse, abort, Api, Resource
from marshmallow import Serializer, fields

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.debug=True
api = restful.Api(app)
db = flask.ext.sqlalchemy.SQLAlchemy(app)

# TODO 
# - parse query incoming parameters YES
# - custom response object YES
# - middleware (auth call, audit, etc...) YES
# - validation YES
# - 


userusergroups = db.Table('userusergroups',
    db.Column('userid', db.Integer, db.ForeignKey('user.id')),
    db.Column('usergroupid', db.Integer, db.ForeignKey('usergroup.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    usergroups = db.relationship('UserGroup', secondary=userusergroups,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
 
class UserGroup(db.Model):
    __tablename__ = 'usergroup'
    id = db.Column(db.String, primary_key=True, autoincrement=False)
    title = db.Column(db.String(80), unique=True)
    enabled = db.Column(db.Boolean, unique=False)
    
    def __init__(self, title, enabled):
        self.title = title
        self.enabled = enabled

    def __repr__(self):
        return '<UserGroup %r>' % self.title

class UserSerializer(Serializer):
    class Meta:
        fields = ('id', 'username', 'email', "usergroups")
        exclude = ('usergroups',)

db.drop_all()
db.create_all()
u1 = User('asdf','user two', 'admin@example.com')
u2 = User('hjkl','user one', 'admin2@example.com')
db.session.add(u1)
db.session.add(u2)
db.session.commit()


class UserResource(restful.Resource):
    def get(self):
        print "list all users"
        return {"message":"not implemented"}, 200

    def post(self):
        print "CREATE user"
        return {"message":"not implemented"}, 200

class UserResourceSpecific(restful.Resource):
    parser = reqparse.RequestParser()

    def put(self, id):
        print "PUT/UPDATE called : %s"%id
        return {"message":"UPDATED"}, 200

    def delete(self, id):
        print "DEL called : %s"%id
        return {"message":"DELETED"}, 200

    def get(self, id):
        print "User get single"
        print "User get : %s"%id
        args = parser.parse_args()

        user = User.query.get(id)
        print dir(user)
        print "User get : %s"%user.id
        print "User get : %s"%user.email

        ser = UserSerializer(user, strict=True)
        print ser.data

        return jsonify( ser.data )

api.add_resource(UserResourceSpecific, '/users/<string:id>')
api.add_resource(UserResource, '/users')


parser = reqparse.RequestParser()
parser.add_argument('expand', type=bool)
parser.add_argument('X-AUTH-THING', type=str, location='headers')

@app.before_request
def before_request():
    args = parser.parse_args()
    auth = args["X-AUTH-THING"]
    print "before request called!, I could call auth : %s"%auth

class HelloWorld(restful.Resource):


    # I can filter the response
    resource_fields = {
        'testid':   fields.String,
        'expand':    fields.Boolean
    }
    
    @marshal_with(resource_fields)
    def get(self, testid):
        print "get route with testid"
        args = parser.parse_args()
        print args
        expand = args["expand"]
        print "url id during call : %s"%testid
        print "url query param : %s"%expand
        return {'hello': 'world', "testid":testid, "expand":expand}, 201

    def post(self):
        print "POST : called"
        return {}

    def put(self, testid):
        print "PUT : called"
        return {}




#api.add_resource(HelloWorld, '/hello/<int:testid>', '/hello')



# start the flask loop
app.run()     