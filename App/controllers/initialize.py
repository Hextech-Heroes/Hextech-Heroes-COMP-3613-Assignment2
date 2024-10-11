from .user import create_user
from .student import create_student
from .review import create_review
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    bob = create_student('bob', 'bobbington')
    create_review(bob, 'Good Job', 'Has done excellent work in class')
    #bob.reviews.append(Review('Good Job', 'Has done excellent work in class'))
    db.session.add(bob)
    db.session.commit()
