from fastapi import FastAPI

# Initialize FastAPI application to serve for ai chat services
app = FastAPI(title="AI Chat Service",
              description="Service that contains all endpoints that represent an AI chat service",
              version="0.1.0",
              openapi_url="/chat-service/openapi.json",
              docs_url="/chat-service/docs",
              redoc_url="/chat-service/redoc",
              swagger_ui_oauth2_redirect_url="/chat-service/docs/oauth2-redirect")
