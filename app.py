from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase("contact-book", user="", password="", host="localhost", port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Contact(BaseModel):
  name = CharField()
  phone_number = BigIntegerField()

db.connect()
db.drop_tables([Contact])
db.create_tables([Contact])

Contact(name="Nichole", phone_number=3475555555).save()
Contact(name="James", phone_number=7185555555).save()
Contact(name="Nicholas", phone_number=2125555555).save()

app = Flask(__name__)

@app.route('/person/', methods=['GET', 'POST'])
@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Contact.get(id)))
    else:
        peopleList = []
        for person in Contact.select():
            peopleList.append(model_to_dict(person))
        return jsonify(peopleList)

  if request.method == 'PUT':
    body = request.get_json()
    Contact.update(body).where(Contact.id ==  id).execute()
    return "Person " + str(id) + " has been updated!"

  if request.method == 'POST':
    body = request.get_json()
    new_person = dict_to_model(Contact, body)
    new_person.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Contact.delete().where(Contact.id == id).execute()
    return "Contact " + str(id) + " has been deleted."

app.run(debug=True, port=9000)