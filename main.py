from app import create_app
import logging

if __name__ == "__main__":
    app = create_app()
    # Set up logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(debug=True)