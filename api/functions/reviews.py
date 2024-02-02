import uuid
from ..config.db import reviews
import json
from datetime import datetime

class ReviewSerializer:
    def __init__(self, event):
        self.review = event['review']

    def serialize_review(self):
        review = {
            '_id':         uuid.uuid4().hex,
            'title':       self.review['title'],
            'rating':      self.review['rating'],
            'description': self.review['description'],
            'user_id':     self.review['user_id'],
            'media_type':  self.review['media_type'],
            'media_id':    self.review['media_id'],
            'created_on':  datetime.now().isoformat(),
            'tags':        ''
        }
        return review

def create_response(data={}, message=None, status=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }

def index_reviews(event, context):
    """Return ALL reviews"""
    return json.dumps({
        'data': {
            'reviews': list(reviews.find({}))
        }
    })

def new_review(event, context):
    review = ReviewSerializer(event).serialize_review()

    review_created = reviews.insert_one(review)
    if review_created.acknowledged:
        return create_response(data=review, message='success', status='201')
    else:
        return create_response(data={}, message='unsuccessful', status='500')

def delete_review(event, context):
    path_parameters = event.get('pathParameters', {})
    review_id = path_parameters.get('review_id')

    review_deleted = reviews.find_one_and_delete({'_id': review_id})
    if review_deleted:
        return create_response(data=review_deleted, message='success', status='204')
    else:
        return create_response(data={}, message=f'No review with ID: {review_id}', status='404')
