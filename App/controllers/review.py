from App.models import Review
from App.database import db

def create_review(student, title, text):
    newReview = Review(title=title, text=text)
    student.reviews.append(newReview)
    db.session.add(student)
    db.session.commit()
    return newReview