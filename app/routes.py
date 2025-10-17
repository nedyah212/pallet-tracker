from flask import Blueprint, render_template, redirect, url_for
from .controllers import Controller

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
  return render_template("home.html", msg=Controller.home())