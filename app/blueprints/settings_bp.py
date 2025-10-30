from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.controllers import SettingsController
from app.services import *
from app.models import *
from app.repositories import *

settings_bp = Blueprint("settings_bp", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingsController.settings()["settings-form"]
    if form.validate_on_submit():

        choice = form.choice.data
        if choice == "pallet":
            route = "settings_bp.pallet"
        elif choice == "trailer":
            route = "settings_bp.trailer"

        return redirect(
            url_for(
                route,
            )
        )
    return render_template("settings/settings.html", form=form)


@settings_bp.route("/settings/pallet", methods=["GET", "POST"])
def pallet():
    form = SettingsController.settings()["batch-form"]
    if form.validate_on_submit():
        msg = StorageServices.add_element(form.choice.data, Pallet)
        if msg != "":
            message, category = msg
            flash(message, category)
        return redirect(url_for("settings_bp.pallet"))

    return render_template("settings/pallet.html", form=form)


@settings_bp.route("/settings/trailer", methods=["GET", "POST"])
def trailer():
    form = SettingsController.settings()["batch-form"]
    if form.validate_on_submit():
        msg = StorageServices.add_element(form.choice.data, Trailer)
        if msg != "":
            message, category = msg
            flash(message, category)

        return redirect(url_for("settings_bp.trailer"))

    return render_template("settings/trailer.html", form=form)
