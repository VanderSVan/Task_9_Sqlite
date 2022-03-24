from flask import make_response, jsonify


def handle_404_error_api(error=None):
    if error:
        return make_response(jsonify({'status': 404, 'message': str(error)}), 404)
    return make_response(jsonify({'status': 404, 'message': 'Not found'}), 404)