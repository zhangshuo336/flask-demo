from flask import Blueprint
orders = Blueprint("orders",__name__,static_folder="static",template_folder="templates")
from .views import orderss


