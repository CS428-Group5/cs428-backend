from ninja import NinjaAPI, Schema, Form
from authentication.api import authenticate_router
from users.api import mentor_router, user_router, expertise_router
from payment.api import payment_router

api = NinjaAPI()


api.add_router("authentication", authenticate_router, tags=["Authentication"])
api.add_router("/mentors/", mentor_router, tags=["Mentors"])
api.add_router("/users/", user_router, tags=["Users"])
api.add_router("/expertises/", expertise_router, tags=["Expertises"])
api.add_router("/payment/", payment_router, tags=["Payment"])
