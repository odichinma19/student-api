from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
students = [
    {"id": 1, "name": "John Doe", "course": "Software Engineering"},
    {"id": 2, "name": "Mary Smith", "course": "Computer Science"}
]

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Student Management API is running"}), 200


# Get all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students), 200


# Get a single student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404


# Add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    new_student = {
        "id": students[-1]["id"] + 1 if students else 1,
        "name": data.get("name"),
        "course": data.get("course")
    }
    students.append(new_student)
    return jsonify(new_student), 201


# Update a student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    student["name"] = data.get("name", student["name"])
    student["course"] = data.get("course", student["course"])

    return jsonify(student), 200


# Delete a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
