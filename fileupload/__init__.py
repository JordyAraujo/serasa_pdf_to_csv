import os

from flask import Flask

from .routes import upload

CNPJ = ' 02.275.901/0001-11'
COMPANY_NAME = 'CDA'


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "project.sqlite"),
    )

    UPLOAD_FOLDER = os.path.join(app.instance_path, "upload")
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    CSV_FOLDER = os.path.join(app.instance_path, "csv")
    app.config['CSV_FOLDER'] = CSV_FOLDER

    app.config['CNPJ'] = CNPJ
    app.config['COMPANY_NAME'] = 'CDA'

    try:
        os.makedirs(app.instance_path)
        os.makedirs(UPLOAD_FOLDER)
        os.makedirs(CSV_FOLDER)
    except OSError:
        pass

    app.register_blueprint(upload.bp)

    return app


app = create_app()