from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import models
from ..schemas import schemas
from keycloak import KeycloakAdmin

# Initialize Keycloak admin client (configure properly in settings)
keycloak_admin = KeycloakAdmin(
    server_url="http://fixnow-keycloak.ddns.net/auth/",
    username="admin",
    password="adminpassword",
    realm_name="Fast-api",
    verify=False
)

def get_service_providers(db: Session):
    return db.query(models.FixNowUser).filter(models.FixNowUser.role == "service_provider").all()


def create_user_with_role(user_data: schemas.FixNowUserCreate, role: str, db: Session):
    try:
        # 1. Create user in Keycloak
        user_id = keycloak_admin.create_user({
            "username": user_data.email,
            "email": user_data.email,
            "enabled": True,
            "firstName": user_data.full_name,
            "credentials": [{"value": user_data.password, "type": "password"}]
        })

        # Sometimes create_user returns None — get ID manually
        if not user_id:
            kc_user = keycloak_admin.get_user_id(user_data.email)
            user_id = kc_user

        # 2. Assign role in Keycloak
        role_obj = keycloak_admin.get_realm_role(role)
        keycloak_admin.assign_realm_roles(user_id=user_id, roles=[role_obj])

        # 3. Save in Postgres
        db_user = models.FixNowUser(
            keycloak_id=user_id,
            full_name=user_data.full_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            role=role,
            service_type=user_data.service_type,
            business_name=user_data.business_name,
            address=user_data.address,
            available_hours=user_data.available_hours,
            emergency_support=user_data.emergency_support,
            hourly_rate=user_data.hourly_rate,
            description=user_data.description,
            experience=user_data.experience,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Keycloak or DB error: {str(e)}")
