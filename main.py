#Import Dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


#define application and database variables
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app_version = "v1/"

#create the data definition
class DataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wtemp = db.Column(db.Float, nullable=False)
    wdescription = db.Column(db.String, nullable=False)
    currency = db.Column(db.Float, nullable=False)
#    brewname = db.Column(db.String, nullable=False)
#    brewurl = db.Column(db.String, nullable=False)
#    brewphone = db.Column(db.String, nullable=False)

#outputs to log/screen to verify data visually
    def __repr__(self):
        return f"Data(wtemp = {wtemp}, wdescription = {wdescription}, currency = {currency})"
    
#run this statement the first thme to create the database structure
# db.create_all()

#handle the incoming data request with a parser
#arguments for a put request
data_put_args = reqparse.RequestParser()
data_put_args.add_argument("wtemp", type=float, help="Temp in Celsius", required=True)
data_put_args.add_argument("wdescription", type=str, help="Weather Description", required=True)
data_put_args.add_argument("currency", type=float, help="Currency in Euros", required=True)

#arguments for an update request
data_update_args = reqparse.RequestParser()
data_update_args.add_argument("wtemp", type=float, help="Temp in Celsius", required=True)
data_update_args.add_argument("wdescription", type=str, help="Weather Description", required=True)
data_update_args.add_argument("currency", type=float, help="Currency in Euros", required=True)

#Map the types to columns extracted from the database object
resource_fields = {
    'id': fields.Integer,
    'wtemp': fields.Float,
    'wdescription': fields.String,
    'currency': fields.Float
}

#Set up the Resource Functions for CRUD
class Data(Resource):
   
    #GET (READ in CRUD)
    #@marshal_with serializes output from the DB as a dictionary (json object) so we can work with it in python
    @marshal_with(resource_fields)
   
    def get(self, data_id):
        result = DataModel.query.filter_by(id=data_id).first()
        if not result:
            abort(404, message="Could not find data with that id")
        return result

    #POST (CREATE in CRUD)
    @marshal_with(resource_fields)
    def put(self, data_id):
        args = data_put_args.parse_args()
        result = DataModel.query.filter_by(id=data_id).first()
        if result:
            abort(409, message="Data id taken...")

        data = DataModel(id=data_id, wtemp=args['wtemp'], wdescription=args['wdescription'], currency=args['currency'])
        db.session.add(data)
        db.session.commit()
        return data, 201
   
    #PUT (UPDATE in CRUD)
    @marshal_with(resource_fields)
    def patch(self, data_id):
        args = data_update_args.parse_args()
        result = DataModel.query.filter_by(id=data_id).first()
        if not result:
            abort(404, message="Data doesn't exist, cannot update")

        if args['wtemp']:
            result.wtemp = args['wtemp']
        if args['wdescription']:
            result.wdescription = args['wdescription']
        if args['currency']:
            result.currency = args['currency']

        db.session.commit()

        return result, 200

    #DELETE (DELETE in CRUD)
    def delete(self, data_id):
        abort_if_data_id_doesnt_exist(data_id)
        del Data[data_id]
        return '', 204

#Register the Resource called video to the API (remember to change versions when making changes for submission)
api.add_resource(Data, "/" + app_version + "video/<int:video_id>")

#Run the API body
if __name__ == "__main__":
    app.run(debug=True)
