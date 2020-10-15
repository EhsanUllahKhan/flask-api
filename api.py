from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()


def selectAllStudents():
    cursor.execute(select_all_students)
    STUDENTS = cursor.fetchall()
    return STUDENTS


class Student(Resource):

    def get(self, student_id):
        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)

        if str(student_id) not in data:
            return "Not found", 404
        else:
            return data[str(student_id)]

    def put(self, student_id):
        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)

        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        if str(student_id) not in data:
            return "Not found", 404
        else:
            student = data[str(student_id)]
            student["name"] = args["name"] if args["name"] is not None else student["name"]
            student["age"] = args["age"] if args["age"] is not None else student["age"]
            student["spec"] = args["spec"] if args["spec"] is not None else student["spec"]
            with open("data.json", "w") as write_file:
                write_file.write(json.dumps(data))
            return student, 200

    def delete(self, student_id):
        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)

        if str(student_id) not in data:
            return "Not found", 404
        else:
            del data[str(student_id)]
            with open("data.json", "w") as write_file:
                write_file.write(json.dumps(data))

            return '', 204


class StudentsList(Resource):
    def get(self):
        return selectAllStudents()

    def post(self):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        values = [
            (args["name"], args["age"], args["spec"])
        ]

        cursor.executemany(insert_query, values)
        db.commit()
        return STUDENTS, 201


STUDENTS = {
}

api.add_resource(Student, '/students/<student_id>')
api.add_resource(StudentsList, '/students/')


if __name__ == "__main__":
    app.run(debug=True)
