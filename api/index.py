try:
    from backend.main import app
except Exception:
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    import traceback
    
    app = FastAPI()
    
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(full_path: str):
        return PlainTextResponse(f"Backend failed to start:\n{traceback.format_exc()}", status_code=500)
