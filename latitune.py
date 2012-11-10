import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy

# for password hashing
from werkzeug.security import generate_password_hash, check_password_hash

app       = Flask (__name__)
app.debug = True

heroku    = Heroku (app)
db        = SQLAlchemy (app)

class API_Response:
  def __init__(self, status="ERR"):
   self.status = status

  def as_dict(self):
    return {"meta":{"status":self.status}, "objects":{}}

# CONTROLLERS

@app.route("/")
def index():
  return "Hello Latitune!"

@app.route("/api/user", methods=['PUT'])
def create_user():
  # try:
    return str(request.args)
    if all ([arg in request.args for arg in ['username', 'email', 'password']]):
      new_user = User(request.args['username'],
                      request.args['email'],
                      request.args['password'])
      db.session.add(new_user)
      db.session.commit()
      return jsonify(API_Response("OK").as_dict())
    # else:
      # raise
  # except:
  #   return jsonify(API_Response("ERR").as_dict())

# MODEL DEFINITIONS
class User(db.Model):
  __tablename__ = 'user'

  id      = db.Column(db.Integer, primary_key = True)
  name    = db.Column(db.String(80), unique = True)
  email   = db.Column(db.String(120), unique = True)
  pw_hash = db.Column(db.String(120))
  blip    = db.relationship("Blip", backref="user")

  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.set_password(password)

  def set_password(self, password):
    self.pw_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pw_hash, password)

class Song(db.Model):
  __tablename__ = 'song'

  id               = db.Column(db.Integer, primary_key = True)
  artist           = db.Column(db.String(80))
  title            = db.Column(db.String(120))
  album            = db.Column(db.String(80))
  provider_song_id = db.Column(db.String(200))
  provider_key     = db.Column(db.Enum('Spotify','Youtube',
                                       name='provider_key'))
  blip             = db.relationship("Blip", backref="song")

class Blip(db.Model):
  __tablename__ = 'blip'

  id        = db.Column(db.Integer, primary_key = True)
  song_id   = db.Column(db.Integer, db.ForeignKey('song.id'))
  user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
  longitude = db.Column(db.Float)
  latitude  = db.Column(db.Float)
  timestamp = db.Column(db.DateTime, default=datetime.now)

# MAIN RUN

if __name__ == "__main__":
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)

