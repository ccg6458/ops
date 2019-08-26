from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .service import CronJob





db = SQLAlchemy()
login_manager = LoginManager()
cron=CronJob()
