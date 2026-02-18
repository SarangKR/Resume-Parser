try:
    from backend.main import app
except Exception:
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    import traceback
    
    app = FastAPI()
    
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        return PlainTextResponse(f"Backend failed to start:\n{traceback.format_exc()}", status_code=500)
