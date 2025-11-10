from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    DateTimeField,
    SelectField,
    TextAreaField
)
from wtforms.validators import DataRequired, Length, Optional


def remove_delimiters(text):
    return (
        text.replace("-", "").replace(" ", "").replace("/", "")
        if text is not None
        else ""
    )


class CreateShipmentForm(FlaskForm):
    registration_number = StringField(
        "Registration Number",
        validators=[DataRequired(), Length(min=1, max=50)],
        filters=[lambda x: remove_delimiters(x)],
    )
    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=1, max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=1, max=30)],
    )
    tag_colour = SelectField(
        "Tag Colour",
        validators=[DataRequired(), Length(min=3, max=15)],
    )
    tag_code = StringField(
        "Tag Code",
        validators=[DataRequired(), Length(min=6, max=30)],
    )
    origin = StringField(
        "Origin",
        validators=[DataRequired(), Length(max=30)],
    )
    destination = StringField(
        "Destination",
        validators=[Optional(), Length(max=30)],
    )
    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(max=250)],
    )
    archived = BooleanField("Archived", default=False)

    submit = SubmitField("Save Shipment")
