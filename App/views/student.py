from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import Student
from ..controllers import (
    create_student,
    get_all_students,
    get_student,
    get_student_by_lName,
    is_admin,
)

student = Blueprint("student", __name__)

@student.route("/student/<id>", methods=["GET"])
@jwt_required()
def search_student(id: str) -> tuple[Response, int]:
    student: Student | None = get_student(id)
    if student is None:
        return jsonify(error="Student not found"), 404
    return jsonify(fName=student.fName, lName=student.lName), 200

@student.route("/students", methods=["GET"])
@jwt_required()
def search_students() -> tuple[Response, int]:
    students: list[Student] = get_all_students()
    return jsonify([{"fName": s.fName, "lName": s.lName} for s in students]), 200

@student.route("/students/<lName>", methods=["GET"])
@jwt_required()
def search_students_by_last_name(lName: str) -> tuple[Response, int]:
    student: Student | None = get_student_by_lName(lName)
    if student is None:
        return jsonify(error="Student not found"), 404
    return jsonify(fName=student.fName, lName=student.lName), 200

@student.route("/student", methods=["POST"])
@jwt_required()
def add_student() -> tuple[Response, int]:
    admin: bool = is_admin(get_jwt_identity())
    if not admin:
        return jsonify(error="Unauthorized"), 401
    data = request.get_json()
    if not data.get("fName") or not data.get("lName"):
        return jsonify(error="Missing required fields"), 400
    student = create_student(data["fName"], data["lName"])
    return jsonify(fName=student.fName, lName=student.lName), 200
