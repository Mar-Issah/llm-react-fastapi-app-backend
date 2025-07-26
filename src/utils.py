# Utility functions for the backend

from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

load_dotenv()


clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))


# This function is intended to be used in FastAPI endpoints to verify users and get their IDs securely.
def authenticate_and_get_user_details(request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            # Just like the CORS middleware, we allow only specific origins to access the API from the Frontend.
            AuthenticateRequestOptions(
                authorized_parties=[
                    "http://localhost:5173",
                    "http://localhost:5174",
                    "http://localhost:3000",
                    "https://llm-mcq.vercel.app",
                ],
                jwt_key=os.getenv("JWT_KEY"),
            ),
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")
        # If the user is not signed in, raise an HTTPException with a 401 status code
        # Else get the subject
        user_id = request_state.payload.get("sub")

        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
