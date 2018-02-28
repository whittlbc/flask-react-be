"""
File for managing/migrating our database

Usage:

  Init new database connection (unnecessary if migrations/ dir already exists)

    $ python manage.py db init

  Create migration files from changes made to src/models.py:

    $ python manage.py db migrate

  Apply migrations to the database:

    $ python manage.py db upgrade

"""
from src import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()