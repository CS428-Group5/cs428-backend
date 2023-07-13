from ninja import NinjaAPI, Schema, Form
from authentication.api import authenticate_router

api = NinjaAPI(csrf=True)
# Add router for each app here
# Ex: api.add_router("/users/", account_router, tags=["Users"])
api.add_router("authentication", authenticate_router)


