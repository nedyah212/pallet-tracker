from .forms import Forms

class Controller:

  def home():
    return "home"

  def create_shipment():
    return Forms.CreateShipmentForm()