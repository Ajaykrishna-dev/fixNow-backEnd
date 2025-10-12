# config.py
import os
from dotenv import load_dotenv
from keycloak import KeycloakAdmin

# Load environment variables at the top level of the application
load_dotenv() 

# Keycloak Settings
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_ADMIN_USERNAME = os.getenv("KEYCLOAK_ADMIN_USERNAME")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")

# Initialize Keycloak admin client once
try:
    keycloak_admin = KeycloakAdmin(
        server_url=KEYCLOAK_SERVER_URL,
        username=KEYCLOAK_ADMIN_USERNAME,
        password=KEYCLOAK_ADMIN_PASSWORD,
        realm_name=KEYCLOAK_REALM_NAME,
        verify=False 
    )
    print("Keycloak Admin Client Initialized Successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not initialize Keycloak Admin Client. Check credentials and server URL. Error: {e}")
    keycloak_admin = None # Set to None for controlled failure

# Add a check to prevent running if credentials failed to load
if not all([KEYCLOAK_SERVER_URL, KEYCLOAK_ADMIN_USERNAME, KEYCLOAK_ADMIN_PASSWORD, KEYCLOAK_REALM_NAME]):
    raise EnvironmentError("One or more Keycloak environment variables are missing. Check your .env file.")