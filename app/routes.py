from flask import Blueprint, render_template, redirect, url_for
from .controllers import Controller
from .services import Services
from .models import Shipment

main = Blueprint("main", __name__)

@main.route("/")
def home():
  return render_template("home.html")

@main.route("/create_shipment", methods=["GET", "POST"])
def create_shipment():

  form = Controller.create_shipment()
  if form.validate_on_submit():
    success = Services.DatabaseMethods.create_shipment(form.data)

    if success:
      return redirect('/')

  return render_template("create_shipment.html", form=form)

@main.route("/show_shipment/<registration_number>")
def show_shipment(registration_number):
  return render_template('show_shipment.html', registration_number=registration_number)

@main.route("/edit_type/<registration_number>")
def edit_shipment_type(registration_number):
  return render_template("edit_shipment_type.html", registration_number=registration_number)

@main.route("/edit_type/<registration_number>/floor")
def type_floor(registration_number):
  return render_template("type_floor.html", registration_number=registration_number)

@main.route("/edit_type/<registration_number>/pallet")
def type_pallet(registration_number):
  return render_template("type_pallet.html", registration_number=registration_number)

@main.route("/edit_type/<registration_number>/trailer")
def type_trailer(registration_number):
  return render_template("type_trailer.html", registration_number=registration_number)

@main.route("/settings")
def settings():
  return render_template("settings.html")

@main.route("/settings/pallet_manager")
def pallet_manager():
  return render_template("pallet_manager.html")

@main.route("/settings/trailer_manager")
def trailer_manager():
  return render_template("trailer_manager.html")