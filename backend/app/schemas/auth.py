from typing import Literal
from pydantic import BaseModel, EmailStr, Field, model_validator
from app.db.models.users import UserRole

class Signup(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    mobile: str | None = Field(default=None, pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr | None = None
    password: str = Field(min_length=8, max_length=72)
    preferred_language: Literal["en", "hi", "or"] = "en"
    state: str = Field(min_length=2, max_length=100)
    district: str = Field(min_length=2, max_length=100)
    locality: str = Field(default="", max_length=150)
    ward_village: str = Field(default="", max_length=150)
    consent: bool
    area: str = ""
    experience: str = ""

    @model_validator(mode="after")
    def validate_signup(self):
        if not self.consent:
            raise ValueError("consent_required")
        if not self.mobile and not self.email:
            raise ValueError("identifier_required")
        if len(self.password.encode("utf8")) > 72:
            raise ValueError("password_too_long")
        return self

class AccessRequestCreate(Signup):
    role_requested: Literal["district_official", "state_planner", "national_planner", "auditor"]
    organization: str = Field(min_length=2, max_length=200)
    designation: str = Field(min_length=2, max_length=150)
    reason: str = Field(min_length=10, max_length=1000)
    verification_info: str = Field(min_length=3, max_length=500)

class LoginRequest(BaseModel):
    identifier: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=72)

class OTPVerify(BaseModel):
    challenge_id: str
    code: str = Field(min_length=6, max_length=6)

class ResetRequest(BaseModel):
    identifier: str = Field(min_length=3, max_length=254)

class ResetConfirm(OTPVerify):
    password: str = Field(min_length=8, max_length=72)

class RefreshRequest(BaseModel):
    refresh_token: str

class ProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    preferred_language: Literal["en", "hi", "or"]
    locality: str = Field(default="", max_length=150)
    ward_village: str = Field(default="", max_length=150)
