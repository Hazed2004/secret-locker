from fastapi.middleware.cors import CORSMiddleware

def middleware_config(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5500", "http://192.168.1.6:5500"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
