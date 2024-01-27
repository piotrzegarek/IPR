from flask.cli import FlaskGroup

from app import app
from app.models import db

cli = FlaskGroup(app)

@cli.command("recreate_db")
def recreate_db():
    '''Recreate the database'''
    db.reflect()
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("create_db")
def create_db():
    '''Create the database'''
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()