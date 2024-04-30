import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)
from supabase import create_client, Client

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.register_blueprint(todos.bp)

    os.environ["SUPABASE_URL"] = "https://pvmbjudbticervnndrvm.supabase.co"
    os.environ["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB2bWJqdWRidGljZXJ2bm5kcnZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ0MDg2ODQsImV4cCI6MjAyOTk4NDY4NH0.6s2kudkT4wwaQfUxRH6TZ5AIdbG-Dt2x0yv9YoIK6O0"

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabaseWrapper: Client = create_client(url, key)

    bp = Blueprint('todos', __name__, url_prefix='/')

    # Endpoints
    @bp.route('/', methods=['GET'])
    def index():
        response = supabaseWrapper.table('todos').select("*").execute()
        data = jsonify(response.data)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return data

    @bp.route('/create', methods=['POST'])
    def create():
        response = supabaseWrapper.table('todos').insert({"task": request.args.get('task'), "is_complete": request.args.get('is_complete')}).execute()
        data = jsonify(response.data)
        return data

    return app