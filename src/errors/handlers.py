from flask import Blueprint, render_template, flash, json

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    response = error.get_response()

    print('---------------------------------------------------')
    print(response.data)
    print('---------------------------------------------------')
    response.content_type = "application/json"

    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    response = error.get_response()

    print('---------------------------------------------------')
    print(response.data)
    print('---------------------------------------------------')
    response.content_type = "application/json"

    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    # flash(message= 'Error(500)', category='error')
    response = error.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    print('---------------------------------------------------')
    print (response.data)
    print('---------------------------------------------------')
    response.content_type = "application/json"

    # return response

    return render_template('errors/500.html'), 500
