from ninja import NinjaAPI, Schema, Form
from authentication.api import authenticate_router

api = NinjaAPI()
api.add_router("authentication", authenticate_router)
# Add router for each app here
# Ex: api.add_router("/users/", account_router, tags=["Users"])

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users don't have the following fields, so provide defaults.
    email: str = None
    first_name: str = None
    last_name: str = None

class Error(Schema):
    message: str

@api.get("/me", response={200: UserSchema, 403: Error})
def me(request):
    return request.user 

@api.post("/login")
def login(request, username: str = Form(...), password: str = Form(...)):
    return {'username': username, 'password': '*****'}


