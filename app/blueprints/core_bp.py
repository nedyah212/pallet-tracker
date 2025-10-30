from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.controllers import ShipmentsController
from app.services import *
from app.models import *
from app.repositories import *

core_bp = Blueprint("core_bp", __name__)


@core_bp.route("/")
def home():
    return render_template("home.html")


@core_bp.route("/create_shipment", methods=["GET", "POST"])
def create_shipment():
    form = ShipmentsController.create_shipment()

    if form.validate_on_submit():
        existing = Shipment.query.filter_by(
            registration_number=form.registration_number.data
        ).first()
        if existing:
            flash(
                "Failed to create shipment, "
                + f"{form.registration_number.data}"
                + " shipment already in the system",
                "error",
            )

        else:
            shipment = StorageServices.create_shipment_object(form)
            success = ShipmentRepository.create_shipment(shipment)
            if success:
                flash(
                    f"Success, Shipment "
                    + f"{shipment.registration_number} "
                    + "added to system.",
                    "success",
                )
                return redirect(
                    url_for(
                        "core_bp.edit_type",
                        registration_number=shipment.registration_number,
                    )
                )
    return render_template("shipment/create.html", form=form)


@core_bp.route("/show_shipment/<registration_number>")
def show_shipment(registration_number):
    return render_template(
        "shipment/show.html", registration_number=registration_number
    )


@core_bp.route("/edit_type/<registration_number>", methods=["GET", "POST"])
def edit_type(registration_number):
    form = ShipmentsController.edit_shipment()

    if form.validate_on_submit():

        choice = form.choice.data
        if choice == "floor":
            route = "core_bp.type_floor"
        elif choice == "pallet":
            route = "core_bp.type_pallet"
        elif choice == "trailer":
            route = "core_bp.type_trailer"

        return redirect(
            url_for(
                route,
                registration_number=registration_number,
            )
        )

    return render_template(
        "shipment/edit_type.html", registration_number=registration_number, form=form
    )


@core_bp.route("/edit_type/<registration_number>/floor", methods=["GET", "POST"])
def type_floor(registration_number):
    data = ShipmentsController.type_floor(registration_number)

    if data["form"].is_submitted():
        # Controller.remove_pallet_or_trailer(data["shipment"], registration_number)
        return redirect(url_for("core_bp.home"))

    return render_template(
        "shipment/type_floor.html", registration_number=registration_number
    )


@core_bp.route("/edit_type/<registration_number>/pallet", methods=["GET", "POST"])
def type_pallet(registration_number):
    data = ShipmentsController.type_pallet(registration_number)

    if data["form"].is_submitted():
        # Controller.remove_pallet_or_trailer(shipment=data["shipment"])
        # Controller.handle_move_to_pallet()  # to implement
        return redirect(url_for("core_bp.home"))

    return render_template(
        "shipment/type_pallet.html",
        registration_number=registration_number,
        form=data["form"],
    )


@core_bp.route("/edit_type/<registration_number>/trailer", methods=["GET", "POST"])
def type_trailer(registration_number):
    data = ShipmentsController.type_trailer(registration_number)

    if data["form"].validate_on_submit():
        ## implement once you have a dropdown for trailer_id on form
        # Controller.handle_move_to_trailer(registration_number=registration_number)
        return redirect(url_for("core_bp.home"))

    return render_template(
        "shipment/type_trailer.html",
        registration_number=registration_number,
        form=data["form"],
    )


@staticmethod
def handle_choice(choice):
    if choice == "floor":
        route = "core_bp.type_floor"
    elif choice == "pallet":
        route = "core_bp.type_pallet"
    elif choice == "trailer":
        route = "core_bp.type_trailer"
    else:
        route = None

    return route
