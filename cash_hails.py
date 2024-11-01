from app import create_app
from os import getenv
from flask import jsonify
from exc import AbortException
from flask.typing import ResponseReturnValue

app = create_app(getenv('CONFIG') or 'default')


# HTTP Error Handlers
@app.errorhandler(404)
def not_found(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'not found'
        }
    }), 404


@app.errorhandler(422)
def invalid_input(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'invalid input'
        }
    }), 422


@app.errorhandler(405)
def method_not_allowed(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'method not allowed'
        }
    }), 405


@app.errorhandler(403)
def forbidded(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'you are forbidden to perform this action'
        }
    }), 403


@app.errorhandler(401)
def unathorized(_: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': {
            'error': 'you are unauthorized to perform this action'
        }
    }), 401


@app.errorhandler(AbortException)
def abort_error(err: Exception) -> ResponseReturnValue:
    return jsonify({
        'status': 'fail',
        'data': err.error
    }), err.code


#status route
@app.route('/status', methods=['GET'])
def app_status() -> ResponseReturnValue:
    """
    Get the status of the application
    """
    return jsonify({
        'status': 'success',
        'data': {
            'app_status': 'active'
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
