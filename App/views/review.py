from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_jwt_extended import jwt_required
from ..controllers import (
    create_review,
    get_all_reviews,
    get_student_reviews,
    get_review
)
from ..models import Review, Student

review = Blueprint("review", __name__)

@review.route("/reviews", methods=["GET"])
@jwt_required()
def get_reviews() -> tuple[Response, int]:
    reviews: list[Review] = get_all_reviews()
    return jsonify([{"id": r.id, "title": r.title, "text": r.text, "student_id": r.student_id} for r in reviews]), 200

@review.route("/reviews/<student_id>", methods=["GET"])
@jwt_required()
def search_student_reviews(student_id: int) -> tuple[Response, int]:
    reviews: list[Review] = get_student_reviews(student_id)
    if not reviews:
        return jsonify(error="No reviews found for this student"), 404
    return jsonify([{"id": r.id, "title": r.title, "text": r.text} for r in reviews]), 200

@review.route("/review", methods=["POST"])
@jwt_required()
def create_new_review() -> tuple[Response, int]:
    data = request.get_json()
    student_id = data.get("student_id")
    title = data.get("title")
    text = data.get("text")
    if not student_id or not title or not text:
        return jsonify(error="Missing required fields"), 400
    
    student: Student | None = Student.query.get(student_id)
    if student is None:
        return jsonify(error="Student not found"), 404
    
    review = create_review(student, title, text)
    return jsonify(id=review.id, title=review.title, text=review.text), 201

@review.route("/review/<id>", methods=["GET"])
@jwt_required()
def search_review(id: int) -> tuple[Response, int]:
    review: Review | None = get_review(id)
    if review is None:
        return jsonify(error="Review not found"), 404
    return jsonify(id=review.id, title=review.title, text=review.text, student_id=review.student_id), 200

