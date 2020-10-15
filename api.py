from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import mysql.connector as mysql

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()


db = mysql.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="studentsdb"
)

# print(db)
cursor = db.cursor()
#cursor.execute("CREATE DATABASE STUDENTSdb")
# cursor.execute("SHOW DATABASES")
# databases = cursor.fetchall()
# print(databases)
# cursor.execute("CREATE TABLE users (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT(11) ,spec VARCHAR(255))")
# cursor.execute("SHOW TABLES")
# tables = cursor.fetchall()
# for table in tables:
#     print(table)


insert_query = "INSERT INTO users (name, age, spec) VALUES (%s, %s, %s)"
select_all_students = "SELECT * FROM users"
select_user_record = "SELECT * FROM users where id=%s "
update_record = "UPDATE users SET name =%s, age=%s, spec=%s WHERE id=%s"
delete_query = "DELETE FROM users WHERE id =%s"


def selectAllStudents():
    cursor.execute(select_all_students)
    STUDENTS = cursor.fetchall()
    return STUDENTS


class Student(Resource):

    def get(self, student_id):
        cursor.execute(select_user_record % student_id)
        return cursor.fetchone()

    def put(self, student_id):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        values = [
            (args["name"], args["age"], args["spec"], student_id)
        ]
        cursor.executemany(update_record, values)
        db.commit()
        return '', 200

    def delete(self, student_id):
        cursor.execute(delete_query % student_id)
        db.commit()
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
