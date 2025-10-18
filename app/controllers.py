from .forms import Forms

class Controller:
  def home():
    return Forms.CreateShipmentForm()