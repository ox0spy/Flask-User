Flask-User API
==============
* `Config Settings`_
* `SQLAlchemyAdapter()`_
* `UserManager`_
* `Template variables`_
* `Template functions`_
* `Signals`_

Config Settings
---------------
.. include:: includes/config_features.txt

.. include:: includes/config_settings.txt

.. include:: includes/config_urls.txt

.. include:: includes/config_email_templates.txt

.. include:: includes/config_form_templates.txt

.. _sqlalchemyadapter:

SQLAlchemyAdapter()
-------------------
Flask-User shields itself from database operations through a DBAdapter.
It ships with a SQLAlchemyAdapter, but the API is very simple, so other adapters
can be easily added.

::

    class SQLAlchemyAdapter(DBAdapter):
        """ This object shields Flask-User from database specific functions. """

        def find_object(self, ObjectClass, **kwargs):
            """ Case sensitive find object by specified kwargs. """

        def ifind_object(self, ObjectClass, **kwargs):
            """ Case INsensitive find object by specified kwargs. """

        def add_object(self, ObjectClass, **kwargs):
            """ Add an object with fields and values specified in kwargs. """

        def update_object(self, object, **kwargs):
            """ Update an object with fields and values specified in kwargs. """

Template variables
------------------
The following template variables are available for use in email and form templates:

.. include:: includes/template_variables.txt

Template functions
------------------
The following template functions are available for use in email and form templates:

.. include:: includes/template_functions.txt

UserManager
-----------

UserManager()
~~~~~~~~~~~~~
::

    user_manager = UserManager(
            db_adapter,                     # typically from SQLAlchemyAdapter()
            app = None,                     # typically from Flask() or None
            change_password_form            = forms.ChangePasswordForm,
            change_username_form            = forms.ChangeUsernameForm,
            forgot_password_form            = forms.ForgotPasswordForm,
            login_form                      = forms.LoginForm,
            register_form                   = forms.RegisterForm,
            reset_password_form             = forms.ResetPasswordForm,
            username_validator              = forms.username_validator,
            password_validator              = forms.password_validator,
            change_password_view_function   = views.change_password,
            change_username_view_function   = views.change_username,
            confirm_email_view_function     = views.confirm_email,
            forgot_password_view_function   = views.forgot_password,
            login_view_function             = views.login,
            logout_view_function            = views.logout,
            register_view_function          = views.register,
            reset_password_view_function    = views.reset_password,
            unauthenticated_view_function   = views.unauthenticated,
            unauthorized_view_function      = views.unauthorized,
            login_manager                   = LoginManager(),
            token_manager                   = tokens.TokenManager(),
            password_crypt_context          = None,
            )

Typical use:

::

    app = Flask(__name__)
    db = SQLAlchemy(app)
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app,
            register_form=my_register_form,
            register_view_function=my_register_view_function)

Work in progress. See :doc:`recipes_basic_app` for now.

init_app()
~~~~~~~~~~
init_app() is used by Application Factories to bind the UserManager to a specific app.

typical use::

    db = SQLAlchemy()
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter)

    def create_app():
        app = Flask(__name__)
        db.init_app(app)
        user_manager.init_app(app)

Work in progress. See :doc:`recipes_basic_app` for now.

hash_password()
~~~~~~~~~~~~~~~
::

    user_manager.hash_password(password)
    # Returns hashed 'password' using the configured password hash
    # Config settings: USER_PASSWORD_HASH_MODE = 'passlib'
    #                  USER_PASSWORD_HASH      = 'bcrypt'
    #                  USER_PASSWORD_SALT      = SECRET_KEY


verify_password()
~~~~~~~~~~~~~~~~~
::

    user_manager.verify_password(password, hashed_password)
    # Returns True if 'password' matches 'hashed password'
    # Returns False otherwise.

Signals
-------
.. include:: includes/signals.txt
