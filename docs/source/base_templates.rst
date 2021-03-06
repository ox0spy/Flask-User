Base templates
==============

**templates/base.html**

All Flask-User forms extend from the template file ``tempates/base.h`` and
Flask-User supplies a built-in version that uses Bootstrap 3.

To make Flask-User use your page template, you will need to create a ``base.html`` template
file in your application's ``templates`` directory.

Use ``{% block content %}{% endblock %}`` as a placeholder for the forms.

**templates/flask_user/public_base.html**

Public forms are forms that do not require a logged-in user:

* ``templates/flask_user/forgot_password.html``,
* ``templates/flask_user/login.html``,
* ``templates/flask_user/register.html``, and
* ``templates/flask_user/reset_password.html``

Public forms extend the template file ``templates/flask_user/public_base.html``,
which by default extends the template file ``templates/base.html``.

If you want the public forms to use a base template file other than ``templates/base.html``,
create the ``templates/flask_user/public_base.html`` file in your application's
``templates`` directory with the following content::

    {% extends 'my_public_base.html' %}

**templates/flask_user/member_base.html**

Member forms are forms that require a logged-in user:

* ``templates/flask_user/change_password.html``, and
* ``templates/flask_user/change_username.html``

Member forms extend the template file ``templates/flask_user/member_base.html``,
which by default extends the template file ``templates/base.html``.

If you want the member forms to use a base template file other than ``templates/base.html``,
create the ``templates/flask_user/member_base.html`` file in your application's
``templates`` directory with the following content::

    {% extends 'my_member_base.html' %}

