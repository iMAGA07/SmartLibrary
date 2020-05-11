import flask
from flask import jsonify, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(
                    only=('id', 'surname', 'name', 'age', 'city_from', 'books_read', 'books_written', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(
                only=('id', 'surname', 'name', 'age', 'city_from', 'books_read', 'books_written', 'email'))
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'city_from', 'books_read', 'books_written', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    users = session.query(User).filter(User.id == user_id).first()
    if users is None:
        return jsonify({'error': 'Id does not exists'})

    users.surname = request.json['surname']
    users.name = request.json['name']
    users.age = request.json['age']
    users.city_from = request.json['city_from']
    users.books_read = request.json['books_read']
    users.books_written = request.json['books_written']
    users.email = request.json['email']
    session.commit()
    return jsonify({'success': 'OK'})
