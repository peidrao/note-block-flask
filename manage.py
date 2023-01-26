from src.server.app import create_app
from src.server.config import config

app = create_app()

if __name__ == "__main__":
    app.run(host=config.HOST, port=8080, debug=config.DEBUG)
