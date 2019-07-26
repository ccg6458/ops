import os

class Config(object):
    # 基础配置
    DEBUG = True
    SECRET_KEY = os.environ.get('WALLE_SECRET', 'mifengkong')
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mifeng888@127.0.0.1:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
