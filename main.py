from json import load, dumps
from replit import db

from flask import Flask, request, redirect, render_template
from wtforms import Form, RadioField
from gevent.pywsgi import WSGIServer

with open("nominee.json") as f:
  nominees = load(f)

class VoteForm(Form):
  pass

for category, people in nominees.items():
  var_name = category.replace(" ", "_")
  setattr(VoteForm, var_name, RadioField(category,
    choices=people
  ))

app = Flask(__name__, static_folder="assets", template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
  vote_form = VoteForm(request.form)

  if not request.headers["X-Replit-User-Id"]:
    return redirect("/login")
  
  if request.headers["X-Replit-User-Name"] in db:
    return render_template("thanks.html")

  if request.method == 'POST' and vote_form.validate():
    data = dumps(vote_form.data)
    db[request.headers["X-Replit-User-Name"]] = data
    return render_template("thanks.html")

  return render_template("vote.html", form=vote_form)

@app.route("/login")
def repl_login():
  return render_template("login.html")

if __name__ == "__main__":
  server = WSGIServer(("0.0.0.0", 8080), app)
  server.serve_forever()
