from flask import Blueprint, render_template, redirect, url_for
from .controllers import Controller

main = Blueprint("main", __name__)

@main.route("/")
def home():
  return render_template("home.html")

@main.route("/create_shipment", methods=["GET", "POST"])
def create_shipment():
  return render_template("create_shipment.html", form=Controller.create_shipment())