from flask import Flask
from routes.main import main_bp

app = Flask(__name__)
app.secret_key = '1234'
app.register_blueprint(main_bp)







