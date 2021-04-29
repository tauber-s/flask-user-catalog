import json
from flask import Response, request, jsonify, abort, make_response
from database.models import User
from database.db import db_psql, db_redis
from flask_restful import Resource
from datetime import datetime, date, timedelta


class UsersApi(Resource):
    def get(self):
        data = get_users(request.args)
        response = make_response(data, 200)
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response

    def post(self):
        try:
            userData = request.get_json()
            user = User(userData['first_name'],
                        userData['last_name'],
                        userData['ssn'],
                        userData['birthday'],
                        userData['gender'],
                        userData['email'])
        except:
            abort(400)

        try:
            res = db_psql.session.add(user)
            db_psql.session.commit()
            status_code = 200
        except:
            db_psql.session.rollback()
            status_code = 500
        
        return make_response(
            jsonify({'user_id': user.id}) if user.id 
                else jsonify({'message': 'Couldn\'t insert user'}),
            status_code
        )
        
class UserApi(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)
        return make_response(
                jsonify({
                'ssn': user.ssn,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'birthday': user.birthday,
                'gender': user.gender,
                'email': user.email,
            }),
            200
        )

def get_from_db(request):
    request = json.loads(request)
    page = request['page'] if 'page' in request else 1
    size = request['size'] if 'page' in request else 50

    query = User.query
    if 'filter[first_name]' in request:
        query = query.filter(User.first_name.ilike('%' + request['filter[first_name]'] + '%'))
    if 'filter[last_name]' in request:
        query = query.filter(User.last_name.ilike('%' + request['filter[last_name]'] + '%'))
    if 'filter[ssn]' in request:
        query = query.filter(User.ssn == request['filter[ssn]'])
    if 'filter[birthday]' in request:
        query = query.filter(User.birthday == request['filter[birthday]'])
    if 'filter[gender]' in request:
        query = query.filter(User.gender.ilike(request['filter[gender]']))
    if 'filter[email]' in request:
        query = query.filter(User.email.ilike('%' + request['filter[email]'] + '%'))

    res = query.paginate(page=page, per_page=size)
    users = {}
    for user in res.items:
        users[user.id] = {
            'id': user.id,
            'ssn': user.ssn,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birthday': user.birthday,
            'gender': user.gender,
            'email': user.email,
        }
    return dict(data=users, 
                   total=res.total, 
                   current_page=res.page,
                   per_page=res.per_page)

def get_from_cache(key: str) -> str:
    val = db_redis.get(json.dumps(key))
    return val

def set_to_cache(key: str, value: str) -> bool:
    state = db_redis.setex(key, timedelta(seconds=3600), value=value)
    return state

def get_users(request, id=None) -> dict:
    request = json.dumps(request)
    data = get_from_cache(key=request)
    if data is not None:
        data = json.loads(data)
        data['cache'] = True

    else:
        data = get_from_db(request)
        if data:
            data['cache'] = False
            state = set_to_cache(key=json.dumps(request), value=json.dumps(data))

    return data
