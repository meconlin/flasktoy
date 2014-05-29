import flask
import flask.ext.sqlalchemy
import flask.ext.restless

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

# TODO 
# - parse query incoming parameters
# - custom response object
# - middleware (auth call, audit, etc...)
# - validation
# - 


userusergroups = db.Table('userusergroups',
    db.Column('userid', db.Integer, db.ForeignKey('user.id')),
    db.Column('usergroupid', db.Integer, db.ForeignKey('usergroup.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    usergroups = db.relationship('UserGroup', secondary=userusergroups,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
 
class UserGroup(db.Model):
    __tablename__ = 'usergroup'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    enabled = db.Column(db.Boolean, unique=False)
    
    def __init__(self, title, enabled):
        self.title = title
        self.enabled = enabled

    def __repr__(self):
        return '<UserGroup %r>' % self.title

db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(User, methods=['GET', 'POST', 'DELETE'])
manager.create_api(UserGroup, methods=['GET', 'POST', 'DELETE'])

# start the flask loop
app.run()     