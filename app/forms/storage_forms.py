from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    SubmitField,
    RadioField,
    SelectField,
    StringField
)
from wtforms.validators import DataRequired, Length


class EditTypeForm(FlaskForm):
    choice = RadioField(
        "Choose an Option",
        choices=[("floor", "Floor"), ("pallet", "Pallet"), ("trailer", "Trailer")],
        validators=[DataRequired()],
        default="pallet",
    )
    submit = SubmitField("Submit")


class BatchEntryForm(FlaskForm):
    choice = TextAreaField(
        "Pallets",
        validators=[DataRequired(message="Please enter pallet data")],
        render_kw={
            "rows": 10,
            "cols": 50,
            "placeholder": "Enter identifier separated by commas",
        },
    )
    submit = SubmitField("Submit")


class EditTypeFloorForm(FlaskForm):
    submit = SubmitField("Set as Floor")


class EditTypeTrailerForm(FlaskForm):
    choice = SelectField("Select an option", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ColourForm(FlaskForm):
    destination = StringField(
        "Enter A Tag Colour",
        validators=[DataRequired(), Length(max=30)],
    )