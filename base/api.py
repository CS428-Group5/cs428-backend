from ninja import NinjaAPI, Schema, Form
from authentication.api import authenticate_router
from users.api import mentor_router, user_router, expertise_router

api = NinjaAPI()
# Add router for each app here
# Ex: api.add_router("/users/", account_router, tags=["Users"])
api.add_router("authentication", authenticate_router, tags=["Authentication"])
api.add_router("/mentors/", mentor_router, tags=["Mentors"])
api.add_router("/users/", user_router, tags=["Users"])
api.add_router("/expertises/", expertise_router, tags=["Expertises"])
