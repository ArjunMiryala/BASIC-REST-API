from flask import Flask, request         #imported request because we need to use info from request example likes:10
from flask_restful import Api, Resource, reqparse, abort , fields, marshal_with 
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)
api = Api(app)  # Wrapping the Flask app in the Flask-RESTful API

# Configure the SQLite database location. A file named `database.db` will be created in the current directory.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize the SQLAlchemy object, which will handle the database interactions.
db = SQLAlchemy(app)

# Define the model (table) structure for the Video table in the database
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column, automatically increments for each new video.
    name = db.Column(db.String(100), nullable=False)  # Name of the video, required field with a max length of 100 characters.
    views = db.Column(db.Integer, nullable=False)  # Number of views on the video, required field.
    likes = db.Column(db.Integer, nullable=False)  # Number of likes on the video, required field.

    # This method is used to provide a string representation of the object (useful for debugging or logs).
    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

# Create the database tables defined by the models. This should be run only once to initialize the database.
"""" db.create_all()"""
#commented out after using once #


"""#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
names = {"Arjun": {"age": 19, "gender": "male"}, "bill": {"age": 25, "gender": "male"}}

# making resource within api
class HelloWorld(Resource):             # we are making a class whcih is a resource.# and this resource has few methods whcih we can overwrite on it 
    def get(self, name,):                #this is what happens when a get request is sent to the certain url 
#                               # inside the get request we put name so that we can acesses any string they typed after hellowworld and do smthn specific with that
        return names[name]   # {key: Value} pair # Everytime we return some information from our api it should be serialisble
    
    def post(self, name):
        return {"data": "Posted"}       # this is for method post.  so it is activated when requests.post(BASE + "Helloworld")  is in code of test.py

# we are returning information in a python dictionary, this type {"data": "Hello World"} represents json format, 
# json is basically python dictionaries, you have key and values. and also you can store another key:value pair inside one value and so on
# we we are returning in json format so we will write aas python dictionary or smthn which is serialisble         
# registing this as a resource 👇
api.add_resource(HelloWorld, "/Helloworld/<string:name>")   # here we add HelloWorld class(resource) to api, and its accessible through url: "/Helloworld"
#                                                   <string:name> this says that we want user to type some string after Helloworld. its passes to request. stored into variable name as string
#                                   # / is a default url  # So we only want to access this when user types in "Helloworld". So "/Helloworld" is the end point
"""#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

video_put_args = reqparse.RequestParser()      # we are making new request parser object # Specifies the expected fields in the request and their validation rules
# what this does is automatically parse through the request thats being sent and make sure it fits guidelines we are about to define and also check if it has correct info in it
# if it has correct info it alowws us to grab the info
video_put_args.add_argument("name", type=str, help="Name of the video is required", required = True)    #"name" must be a string.#     # required = Trueis making these as compulsory 
video_put_args.add_argument("views", type=int, help="views on the video is required", required = True)    #"views" must be an integer.#      
video_put_args.add_argument("likes", type=int, help="likes on the video is required", required = True) #"likes" must also be an integer.#
#What request parser Does:
#When a request is made, the parser will check if these fields are present and if their values match the specified type.
#If an argument is missing or has the wrong type, an error message is sent back automatically. The help string will be included in the error message to indicate the issue.#
'''videos = {}

def abort_if_video_ID_doesnt_exist(video_id):
    if video_id not in videos:      #To check if a given video_id exists in the videos dictionary
        abort(404, message="video ID is not valid...") #If it doesn't exist, the function terminates the request and returns an error response #404 is a status code

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message = "video already exists with that ID....")'''
# Used for parsing PATCH requests (Updating an existing video)  
video_update_args = reqparse.RequestParser()  
video_update_args.add_argument("name", type=str, help="Name of the video is required")  
video_update_args.add_argument("views", type=int, help="Views on the video are required")  
video_update_args.add_argument("likes", type=int, help="Likes on the video are required")  

# **Define response fields for API serialization**  
Resource_fields = {  
    'id': fields.Integer,  
    'name': fields.String,  
    'views': fields.Integer,  
    'likes': fields.Integer,  
}  

# **Video Resource (Handles API requests for /video/<int:video_id>)**  
class Video(Resource):  
    @marshal_with(Resource_fields)  # Serialize output to JSON  
    def get(self, video_id):  
        """Fetch a video by ID."""  
        result = VideoModel.query.filter_by(id=video_id).first()  # Search for video in DB  
        if not result:  
            abort(404, message="Could not find video with that ID")  # If video not found, return 404 error  
        return result  # Return video details  

    @marshal_with(Resource_fields)  
    def put(self, video_id):  
        """Create a new video entry."""  
        args = video_put_args.parse_args()  # Validate input request  
        result = VideoModel.query.filter_by(id=video_id).first()  
        if result:  
            abort(409, message="Video ID already taken...")  # Prevent duplicate entries  

        # Create new video entry in the database  
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])  
        db.session.add(video)  # Add video to DB session  
        db.session.commit()  # Save changes to DB  

        return video, 201  # Return newly created video with status code 201 (Created)  

    @marshal_with(Resource_fields)  
    def patch(self, video_id):  
        """Update an existing video entry."""  
        args = video_update_args.parse_args()  # Validate input request  
        result = VideoModel.query.filter_by(id=video_id).first()  # Find the video  
        if not result:  
            abort(404, message="Video doesn't exist, cannot update")  # Return error if not found  

        # Update only provided fields  
        if args['name']:  
            result.name = args['name']  
        if args['views']:  
            result.views = args['views']  
        if args['likes']:  
            result.likes = args['likes']  

        db.session.commit()  # Save updates to DB  
        return result  # Return updated video  

# **Register Video resource with API**  
api.add_resource(Video, "/video/<int:video_id>")  # API endpoint: /video/<video_id>  


if __name__ == "__main__":       # Starting our server and also start flask application 
    app.run(debug=True)          # debug=true indicates it is in debug mode(if anything goes wrong with output and logging info and anything else we will know why)
#                                  # use debug inly in testing environment or devolpment environment       # run on command prompt to check if this works        
