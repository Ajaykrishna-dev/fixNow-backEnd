from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import models
from ..schemas import schemas
from .config import keycloak_admin  # Preconfigured Keycloak client


def get_service_providers(db: Session):
    """Fetch all service providers from the local database."""
    return db.query(models.FixNowUser).filter(models.FixNowUser.role == "service_providers").all()


def create_user_with_role(user_data: schemas.FixNowUserCreate, role: str, db: Session):
    """
    Creates a new user in Keycloak, assigns them a specific role, and saves them in the local DB.
    Mirrors the behavior of your working standalone script.
    """
    user_id = None
    ROLE_TO_ASSIGN = role  # dynamic role (e.g., "service_providers")
    print("DEBUG ROLE:", role)

    # --- 1️⃣ Check if user already exists in Keycloak ---
    try:
        existing_users = keycloak_admin.get_users({"email": user_data.email, "exact": True})
        if existing_users:
            raise HTTPException(status_code=409, detail="User with this email already exists in Keycloak.")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking for existing user in Keycloak. Check connection or credentials. Detail: {e}"
        )

    # --- 2️⃣ Create new user in Keycloak ---
    try:
        new_user_payload = {
            "username": user_data.email,
            "email": user_data.email,
            "enabled": True,
            "firstName": user_data.full_name,
            "lastName": "",  # optional, can extend schema later
            "credentials": [{
                "type": "password",
                "value": user_data.password,
                "temporary": False
            }]
        }

        user_id = keycloak_admin.create_user(new_user_payload)

        # Fallback if Keycloak doesn’t return ID directly
        if not user_id:
            user_id = keycloak_admin.get_user_id(user_data.email)
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to create user or retrieve its ID from Keycloak.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user in Keycloak: {e}")

    # --- 3️⃣ Fetch and assign Keycloak role ---
    try:
        role_obj = keycloak_admin.get_realm_role(ROLE_TO_ASSIGN)
        if not role_obj:
            raise HTTPException(status_code=400, detail=f"Role '{ROLE_TO_ASSIGN}' not found in realm.")

        keycloak_admin.assign_realm_roles(user_id=user_id, roles=[role_obj])

    except Exception as e:
        # If role assignment fails → rollback Keycloak user
        try:
            keycloak_admin.delete_user(user_id=user_id)
        except Exception as rollback_error:
            print(f"CRITICAL: Failed to rollback user {user_id} in Keycloak. {rollback_error}")
        raise HTTPException(status_code=500, detail=f"Error assigning role '{ROLE_TO_ASSIGN}' in Keycloak: {e}")

    # --- 4️⃣ Save user locally in PostgreSQL ---
    try:
        db_user = models.FixNowUser(
            keycloak_id=user_id,
            full_name=user_data.full_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            role=ROLE_TO_ASSIGN,  # ✅ save the same role name locally
            service_type=user_data.service_type,
            business_name=user_data.business_name,
            address=user_data.address,
            available_hours=user_data.available_hours,
            emergency_support=user_data.emergency_support,
            hourly_rate=user_data.hourly_rate,
            description=user_data.description,
            experience=user_data.experience,
            latitude=user_data.latitude,
            longitude=user_data.longitude
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        # If DB commit fails → rollback Keycloak user to maintain consistency
        try:
            keycloak_admin.delete_user(user_id=user_id)
        except Exception as rollback_error:
            print(f"CRITICAL: Failed to rollback user {user_id} in Keycloak after DB failure. {rollback_error}")
        raise HTTPException(status_code=500, detail=f"Database error during user creation: {e}")
