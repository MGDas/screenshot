from flask.cli import FlaskGroup

from app import create_app
from config import Config


app = create_app()
app.config.from_object(Config)

cli = FlaskGroup(app)


if __name__ == '__main__':
    cli()
