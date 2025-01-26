import uvicorn as uv

from src import create_app

if __name__ == "__main__":
    app = create_app()
    uv.run(app)
