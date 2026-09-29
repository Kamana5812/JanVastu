"""Google Identity Services token validation; no account is auto-provisioned."""
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from app.core.config import settings
def verify(credential):
    claims=id_token.verify_oauth2_token(credential,Request(),settings.GOOGLE_CLIENT_ID)
    if not claims.get("email_verified") or not claims.get("sub"):raise ValueError("Unverified identity")
    # Google is authoritative for Gmail and Workspace addresses only.
    if not claims.get("hd") and not claims.get("email","").endswith("@gmail.com"):raise ValueError("Use password login")
    return claims
