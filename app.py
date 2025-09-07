from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection string

app.config["MONGO_URI"] = "mongodb+srv://sakshikumarigungun_db_user:FcTpQ62biH5L35fh@cluster0.7qhshxz.mongodb.net/feedbackDB?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Reference to the collection
feedback_collection = mongo.db.feedbacks

@app.route('/')
def home():
    return jsonify({"message": "Feedback API is running!"})

# Endpoint to submit feedback
@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.get_json()

    # Validate input
    name = data.get('name')
    email = data.get('email')
    feedback_text = data.get('feedback')
    rating = data.get('rating')

    if not name or not email or not feedback_text or rating is None:
        return jsonify({"error": "All fields are required"}), 400

    feedback_data = {
        "name": name,
        "email": email,
        "feedback": feedback_text,
        "rating": rating,
        "date_created": datetime.utcnow()
    }
#this line to insert daata
    result = feedback_collection.insert_one(feedback_data)

    return jsonify({
        "message": "Feedback saved successfully",
        "feedback_id": str(result.inserted_id)
    }), 201

# Endpoint to get all feedbacks (Optional)
@app.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = []
    for fb in feedback_collection.find():
        feedbacks.append({
            "id": str(fb['_id']),
            "name": fb['name'],
            "email": fb['email'],
            "feedback": fb['feedback'],
            "rating": fb['rating'],
            "date_created": fb['date_created'].strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(feedbacks)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
