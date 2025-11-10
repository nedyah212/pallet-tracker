from app.forms import BatchEntryForm, ColourForm


class SettingsController:

    @staticmethod
    def settings():
        return {
            "batch-form": BatchEntryForm(),
            "colour-form": ColourForm()
        }
