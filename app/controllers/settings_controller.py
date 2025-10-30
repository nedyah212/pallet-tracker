from app.forms import EditSettingForm, BatchEntryForm


class SettingsController:

    @staticmethod
    def settings():
        return {
            "settings-form": EditSettingForm(),
            "batch-form": BatchEntryForm(),
        }
