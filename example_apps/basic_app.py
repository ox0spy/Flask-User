from flask import Flask, render_template_string, request
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter

# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'               # Change this for production!!!
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'  # Use Sqlite file db
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password features
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'

    # Configure Flask-User
    USER_ENABLE_USERNAME         = True             # Register and Login with username
    USER_ENABLE_CONFIRM_EMAIL    = True             # Require Email confirmation
    USER_ENABLE_CHANGE_USERNAME  = True
    USER_ENABLE_CHANGE_PASSWORD  = True
    USER_ENABLE_FORGOT_PASSWORD  = True
    USER_ENABLE_RETYPE_PASSWORD  = True

def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    try: app.config.from_object('local_settings')
    except: pass

    # Over-write app config                         # For automated tests
    if test_config:
        for key, value in test_config.items():
            app.config[key] = value

    # Setup Flask-Mail, Flask-Babel and Flask-SQLAlchemy
    app.mail = Mail(app)
    app.babel = babel = Babel(app)
    app.db = db = SQLAlchemy(app)

    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        email = db.Column(db.String(255), nullable=True, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        username = db.Column(db.String(50), nullable=True, unique=True)
        confirmed_at = db.Column(db.DateTime())
        reset_password_token = db.Column(db.String(100), nullable=False, default='')
    app.User = User

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # The '/' page is accessible to anyone
    @app.route('/')
    def home_page():
        if current_user.is_authenticated():
            return profile_page()
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
            <h2>{%trans%}Home Page{%endtrans%}</h2>
            <p><a href="{{ url_for('user.login') }}">{%trans%}Sign in{%endtrans%}</a></p>
            {% endblock %}
            """)

    # The '/profile' page requires a logged-in user
    @app.route('/profile')
    @login_required                                 # Use of @login_required decorator
    def profile_page():
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>{%trans%}Profile Page{%endtrans%}</h2>
                <p> {%trans%}Hello{%endtrans%}
                    {{ current_user.username or current_user.email }},</p>
                <p> <a href="{{ url_for('user.change_username') }}">
                    {%trans%}Change username{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.change_password') }}">
                    {%trans%}Change password{%endtrans%}</a></p>
                <p> <a href="{{ url_for('user.logout') }}?next={{ url_for('user.login') }}">
                    {%trans%}Sign out{%endtrans%}</a></p>
            {% endblock %}
            """)

    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

