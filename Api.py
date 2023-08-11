from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

#Initialising the Api, Db, Schema for the App , Flask Server
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:Root@localhost:3306/learning'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

#Creating Table for the db 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    yash_id = db.Column(db.Integer())
    joined_year = db.Column(db.Integer())

#Schema for the Db Model
class PostSchema(ma.Schema):
    class Meta:
        fields = ("id","name","yash_id","joined_year")
        model = User

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


#CRUD Operations
class UserList(Resource):

    #getting Every user in the list
    def get(self):
        lists = User.query.all()
        return posts_schema.dump(lists)
    
    #Adding new User 
    def post(self):
        new_user = User(
            name = request.json['name'],
            yash_id = request.json['yash_id'],
            joined_year = request.json['joined_year']
        )
        db.session.add(new_user)
        db.session.commit()
        return post_schema(new_user)

class UserResources(Resource):
    #Getting User by their Id
    def get(self, user_id):
        post = User.query.get_or_404(user_id)
        return post_schema.dump(post)
    
    def delete(self, user_id):
        post = User.query.get_or_404(user_id)
        db.session.delete(post)
        db.session.commit()
        return '' , 204

api.add_resource(UserList, '/lists')
api.add_resource(UserResources, '/lists/<int:user_id>')

if __name__ == "__main__":
     with app.app_context():
        db.create_all()

        app.run(debug=True)



