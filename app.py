from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_jwt_extended import create_access_token,jwt_required,JWTManager,get_jwt_identity
app = Flask(__name__)

app.config['SECRET_KEY']='SUPER_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
api=Api(app)
jwt=JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
with app.app_context():
    db.create_all()    


class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        if not username or not password:
            return {'msg':'Missing username and password'},400

        if User.query.filter_by(username=username).first()    :
            return{'msg':'username already exist'},400
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'msg':'User created successfully'},200
    
class UserLogin(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']   
        user =  User.query.filter_by(username=username).first() 
        if user and user.password == password:
            access_token=create_access_token(identity=user.id)
            return{'access_token':access_token},200
        
        return {'msg':'Invalid Credentials'},401
    
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        currunt_user_id=get_jwt_identity()
        return {'msg':f"hello user {currunt_user_id},you accessed the protected resource"},200

api.add_resource(UserRegistration,'/register')        
api.add_resource(UserLogin,'/login')        
api.add_resource(ProtectedResource,'/secure')        



if __name__ == '__main__':
    app.run(debug=True)