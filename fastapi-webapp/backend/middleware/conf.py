from fastapi.middleware.cors import CORSMiddleware

def middleware_config(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8888"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
