import json

fieldnames = ['id', 'name', 'age', 'spec']


data = {}

with open('data.json') as json_file:
    data = json.load(json_file)


def delete(student_id):
    if student_id not in data:
        return "Not found", 404
    else:
        del data[student_id]
        with open("data.json", "w") as write_file:
            write_file.write(json.dumps(data))

        return '', 204


print(len(data))
delete('5')
