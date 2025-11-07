from app.forms import BatchEntryForm


class SettingsController:

    @staticmethod
    def settings():
        return {
            "batch-form": BatchEntryForm(),
        }
