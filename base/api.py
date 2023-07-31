from ninja import NinjaAPI, Schema, Form
from authentication.api import authenticate_router
from users.api import mentor_router, user_router, expertise_router
from google_oauth2.api import google_oauth2_router
from session.api import session_router

api = NinjaAPI()
# Add router for each app here
# Ex: api.add_router("/users/", account_router, tags=["Users"])
api.add_router("authentication", authenticate_router, tags=["Authentication"])
api.add_router("/mentors/", mentor_router, tags=["Mentors"])
api.add_router("/users/", user_router, tags=["Users"])
api.add_router("/expertises/", expertise_router, tags=["Expertises"])
api.add_router("/google-oauth2/", google_oauth2_router, tags=["Google-Oauth2"])
api.add_router("/session/", session_router, tags=["Session"])