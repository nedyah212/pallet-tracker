from .logging import logger

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField

class CreateShipmentForm(FlaskForm):

    registration_number = StringField(
        "Registration Number",
        validators=[DataRequired(), Length(min=1, max=50)],
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
        validators=[Optional(), Length(max=15)],
    )
    tag_code = StringField(
        "Tag Code",
        validators=[Optional(), Length(max=30)],
    )
    date_received = DateTimeField(
        "Date Received",
        format="%Y-%m-%d %H:%M:%S",
        validators=[Optional()],
    )
    date_out = DateTimeField(
        "Date Out",
        format="%Y-%m-%d %H:%M:%S",
        validators=[Optional()],
    )
    origin = StringField(
        "Origin",
        validators=[Optional(), Length(max=30)],
    )
    destination = StringField(
        "Destination",
        validators=[Optional(), Length(max=30)],
    )
    driver_in = StringField(
        "Driver In",
        validators=[Optional(), Length(max=30)],
    )
    driver_out = StringField(
        "Driver Out",
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

    archived = BooleanField("Archived", default=False)
    submit = SubmitField("Save Shipment")