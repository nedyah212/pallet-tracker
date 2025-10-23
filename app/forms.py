from datetime import datetime
from .logging import logger
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField, RadioField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from .models import Shipment
from .services import Services


class Forms:

    class CreateShipmentForm(FlaskForm):

        registration_number = StringField(
            "Registration Number",
            validators=[DataRequired(), Length(min=1, max=50)],
            filters=[Services.HelperMethods.remove_delimiters],
        )
        first_name = StringField(
            "First Name",
            validators=[DataRequired(), Length(min=1, max=30)],
        )
        last_name = StringField(
            "Last Name",
            validators=[DataRequired(), Length(min=1, max=30)],
        )
        tag_colour = StringField(
            "Tag Colour",
            validators=[DataRequired(), Length(min=3, max=15)],
        )
        tag_code = StringField(
            "Tag Code",
            validators=[DataRequired(), Length(min=6, max=30)],
        )
        date_received = DateTimeField(
            "Date Received",
            format="%Y-%m-%d %H:%M:%S",
            validators=[DataRequired()],
            default=datetime.now,
        )
        date_out = DateTimeField(
            "Date Out",
            format="%Y-%m-%d %H:%M:%S",
            validators=[Optional()],
        )
        origin = StringField(
            "Origin",
            validators=[DataRequired(), Length(max=30)],
        )
        destination = StringField(
            "Destination",
            validators=[Optional(), Length(max=30)],
        )
        driver_in = StringField(
            "Driver In",
            validators=[Optional(), Length(max=30)],
        )
        checked_in_by = StringField(
            "Checked In By",
            validators=[Optional(), Length(max=30)],
        )
        checked_out_by = StringField(
            "Checked Out By",
            validators=[Optional(), Length(max=30)],
        )
        driver_out = StringField(
            "Driver Out",
            validators=[Optional(), Length(max=30)],
        )

        archived = BooleanField("Archived", default=False)

        submit = SubmitField("Save Shipment")

        def validate_registration_number(self, registration_number):
            shipment = Shipment.query.filter_by(
                registration_number=registration_number.data
            ).first()
            if shipment:
                logger.warning(
                    f"ConstraintViolation: {registration_number.data} allready exists in the database"
                )
                raise ValidationError("The registration number must be unique.")

    class EditTypeForm(FlaskForm):
        choice = RadioField(
            "Choose an Option",
            choices=[("floor", "Floor"), ("pallet", "Pallet"), ("trailer", "Trailer")],
            validators=[DataRequired()],
        )
        submit = SubmitField("Submit")

    class EditTypeFloorForm(FlaskForm):
        submit = SubmitField("Set as Floor")

    class EditTypePalletForm(FlaskForm):
        submit = SubmitField("Set as Pallet")

    class EditTypeTrailerForm(FlaskForm):
        submit = SubmitField("Set as Trailer")
