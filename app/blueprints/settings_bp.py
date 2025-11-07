from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.controllers import SettingsController
from app.services import *
from app.models import *
from app.repositories import *
from ..logging import logger

settings_bp = Blueprint("settings_bp", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("settings/settings.html")


@settings_bp.route("/settings/pallet", methods=["GET", "POST"])
def pallet():
    form = SettingsController.settings()["batch-form"]
    if form.validate_on_submit():
        msg = StorageServices.add_element(form.choice.data, Pallet)
        message, category = msg
        flash(message, category)
        return redirect(url_for("settings_bp.pallet"))

    return render_template("settings/pallet.html", form=form)


@settings_bp.route("/settings/trailer", methods=["GET", "POST"])
def trailer():
    form = SettingsController.settings()["batch-form"]
    if form.validate_on_submit():
        logger.debug("The form was validated")
        msg = StorageServices.add_element(form.choice.data, Trailer)
        message, category = msg
        print(message)
        flash(message, category)

        return redirect(url_for("settings_bp.trailer"))
    logger.debug("Check")
    return render_template("settings/trailer.html", form=form)
