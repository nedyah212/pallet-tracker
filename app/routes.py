from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.controllers import *
from app.services import *
from app.models import *
from app.repositories import *

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/create_shipment", methods=["GET", "POST"])
def create_shipment():
    form = Controller.create_shipment()

    if form.validate_on_submit():
        existing = Shipment.query.filter_by(
            registration_number=form.registration_number.data
        ).first()
        print(existing)
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
                        "main.edit_type",
                        registration_number=shipment.registration_number,
                    )
                )
    return render_template("shipment/create.html", form=form)


@main.route("/show_shipment/<registration_number>")
def show_shipment(registration_number):
    return render_template(
        "shipment/show.html", registration_number=registration_number
    )


@main.route("/edit_type/<registration_number>", methods=["GET", "POST"])
def edit_type(registration_number):
    form = Controller.edit_shipment()

    if form.validate_on_submit():
        return redirect(
            url_for(
                handle_choice(form.choice.data, alt=True),
                registration_number=registration_number,
            )
        )

    return render_template(
        "shipment/edit_type.html", registration_number=registration_number, form=form
    )


@main.route("/edit_type/<registration_number>/floor", methods=["GET", "POST"])
def type_floor(registration_number):
    data = Controller.type_floor(registration_number)

    if data["form"].is_submitted():
        # Controller.remove_pallet_or_trailer(data["shipment"], registration_number)
        return redirect(url_for("main.home"))

    return render_template(
        "shipment/type_floor.html", registration_number=registration_number
    )


@main.route("/edit_type/<registration_number>/pallet", methods=["GET", "POST"])
def type_pallet(registration_number):
    data = Controller.type_pallet(registration_number)

    if data["form"].is_submitted():
        # Controller.remove_pallet_or_trailer(shipment=data["shipment"])
        # Controller.handle_move_to_pallet()  # to implement
        return redirect(url_for("main.home"))

    return render_template(
        "shipment/type_pallet.html",
        registration_number=registration_number,
        form=data["form"],
    )


@main.route("/edit_type/<registration_number>/trailer", methods=["GET", "POST"])
def type_trailer(registration_number):
    data = Controller.type_trailer(registration_number)

    if data["form"].validate_on_submit():
        ## implement once you have a dropdown for trailer_id on form
        # Controller.handle_move_to_trailer(registration_number=registration_number)
        return redirect(url_for("main.home"))

    return render_template(
        "shipment/type_trailer.html",
        registration_number=registration_number,
        form=data["form"],
    )


@main.route("/settings", methods=["GET", "POST"])
def settings():
    form = Controller.settings()["settings-form"]
    if form.validate_on_submit():
        return redirect(
            url_for(
                handle_choice(form.choice.data),
            )
        )
    return render_template("settings/settings.html", form=form)


@main.route("/settings/pallet", methods=["GET", "POST"])
def pallet():
    form = Controller.settings()["batch-form"]
    if form.validate_on_submit():
        msg = StorageServices.add_element(form.choice.data, Pallet)
        if msg != "":
            message, category = msg
            flash(message, category)
        return redirect(url_for("main.pallet"))

    return render_template("settings/pallet.html", form=form)


@main.route("/settings/trailer", methods=["GET", "POST"])
def trailer():
    form = Controller.settings()["batch-form"]
    if form.validate_on_submit():
        msg = StorageServices.add_element(form.choice.data, Trailer)
        if msg != "":
            message, category = msg
            flash(message, category)

        return redirect(url_for("main.trailer"))

    return render_template("settings/trailer.html", form=form)


@staticmethod
def handle_choice(choice, alt=False):
    if choice == "floor":
        route = "main.type_floor"
    elif choice == "pallet":
        route = "main.type_pallet" if alt else "main.pallet"
    elif choice == "trailer":
        route = "main.type_trailer" if alt else "main.trailer"
    else:
        route = None

    return route
