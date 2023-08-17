from flask import Blueprint, request, jsonify
from src.api.urls import Endpoint
from src.api import HttpMethod
from datetime import datetime
from src.common.utils.alchemy import execute_sql, execute_sql1
from src.common.utils.social_jwt import encode, decode
user = Blueprint("user", __name__)


@user.route(Endpoint.USER, methods=[HttpMethod.POST])
def sign_up():
    data = request.get_json()
    name = data.get("user", {}).get("name")
    username = data.get("user", {}).get("username")
    password = data.get("user", {}).get("password")
    state = f"""INSERT INTO social_app.user(name,username,password) VALUES ('{name}','{username}','{password}')"""
    if check_username(username):
        return jsonify({"message": "username was existed"})
    else:
        execute_sql1(state)
        return {"user": {
                "name": f"{name}",
                "username": f"{username}",
                "password": f"{password}",
                "bio": None,
                "image": None,
                }
                }


def check_username(username):
    state = f"""SELECT username FROM social_app.user WHERE username = ('{username}')"""
    result = execute_sql(state)
    if result:
        return True
    else:
        return False


@user.route(Endpoint.USER1, methods=[HttpMethod.POST])
def login():
    data = request.get_json()
    data = data.get("user", {})
    username = data.get("username")
    password = data.get("password")
    user_credentials = {"username": username}
    if check_username(username):
        if check_password(username, password):
            token = encode(user_credentials)
            state = f"""SELECT name,bio,image FROM social_app.user WHERE username =('{username}')"""
            result = execute_sql(state)
            name = result[0]['name']
            bio = result[0]['bio']
            image = result[0]['image']
            return {"user": {
                    "name": f"{name}",
                    "token": f"{token}",
                    "username": f"{username}",
                    "password": f"{password}",
                    "bio": f"{bio}",
                    "image": f"{image}"
                    }
                    }
        else:
            return jsonify({"message": "check your password again"})
    else:
        return jsonify({"message": "user did not existed"})


def check_username(username):
    state = f"""SELECT username FROM social_app.user WHERE username = ('{username}')"""
    result = execute_sql(state)
    if result:
        return True
    else:
        return False


def check_password(username, password):
    state = f"""SELECT password FROM social_app.user WHERE username = ('{username}')"""
    result = execute_sql(state)
    result = result[0]['password']
    if password == result:
        return True
    else:
        return False


@user.route(Endpoint.USER, methods=[HttpMethod.GET])
def get_current_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if username:
        state = f"""SELECT * FROM social_app.user WHERE username =('{username}')"""
        result = execute_sql(state)
        name = result[0]['name']
        password = result[0]['password']
        bio = result[0]['bio']
        image = result[0]['image']
        return {"user": {
                "name": f"{name}",
                "token": f"{token}",
                "username": f"{username}",
                "password": f"{password}",
                "bio": f"{bio}",
                "image": f"{image}"
                }
                }
    return jsonify({"message": "check your token"})


@user.route(Endpoint.USER, methods=[HttpMethod.PUT])
def update_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT * FROM social_app.user WHERE username =('{username}')"""
    result = execute_sql(state)
    name = result[0]['name']
    password = result[0]['password']
    data = request.get_json()
    data = data.get('user', {})
    new_name = data.get('name')
    new_bio = data.get('bio')
    new_image = data.get('image')
    new_password = data.get('password')
    if not new_name:
        if not new_password:

            state = f"""UPDATE social_app.user SET name =('{name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{password}') 
            WHERE username=('{username}')"""
            execute_sql1(state)

        else:
            state = f"""UPDATE social_app.user SET name =('{name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{new_password}') 
            WHERE username=('{username}')"""
            execute_sql1(state)

    else:
        state = f"""UPDATE social_app.user SET name =('{new_name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{new_password}') 
        WHERE username=('{username}')"""
        execute_sql1(state)

    if new_name:
        if not new_password:
            state = f"""UPDATE social_app.user SET name =('{new_name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{password}') 
            WHERE username=('{username}')"""
            execute_sql1(state)
    execute_sql1(state)
    result = get_current_user()
    return result


@user.route(Endpoint.PROFILE, methods=[HttpMethod.GET])
def get_profile_current_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT * FROM social_app.user WHERE username = ('{username}')"""
    result1 = execute_sql(state)
    id = result1[0]['id']
    del result1[0]['username']
    del result1[0]['password']
    del result1[0]['id']
    state = f"""SELECT
        article.ID,
        article.title,
        article.body,
        article.created_at,
        article.image,
        COUNT ( favorited_article.id_article ) AS favorites_count 
        FROM
            social_app.article AS article
            LEFT JOIN social_app.favorited_article ON favorited_article.id_article = article.ID 
        WHERE 
            article.id_author = ('{id}')
        GROUP BY
            article.ID,
            article.title,
            article.body,
            article.created_at"""

    result = execute_sql(state)
    return {"profile": result1,
            "articles": result}




@user.route(Endpoint.PROFILE1, methods=[HttpMethod.GET])
def get_profile_user_with_condition():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    result = respond_para()
    for i in result:
        state1 = f"""SELECT * FROM social_app.user WHERE id = ('{i}')"""
        result1 = execute_sql(state1)
        del result1[0]['username']
        del result1[0]['password']
        del result1[0]['id']
        state = f"""SELECT
        article.ID,
        article.title,
        article.body,
        article.created_at,
        article.image,
        COUNT ( favorited_article.id_article ) AS favorites_count 
        FROM
            social_app.article AS article
            LEFT JOIN social_app.favorited_article ON favorited_article.id_article = article.ID 
        WHERE 
            article.id_author = ('{i}')
        GROUP BY
            article.ID,
            article.title,
            article.body,
            article.created_at"""

        result = execute_sql(state)
        return {"profile": result1,
                "articles": result}


def respond_para():
    get_by_name = request.args.get('name')
    state = "SELECT name,id FROM social_app.user "
    result = execute_sql(state)
    dic = {}
    lit = []
    for i in result:
        if get_by_name in i['name']:
            dic[i['name']] = i['id']
    for j in dic.values():
        lit.append(j)
    return lit


@user.route(Endpoint.USER2, methods=[HttpMethod.GET])
def get_notification():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"SELECT id FROM social_app.user WHERE username = '{username}'"
    result = execute_sql(state)
    id = result[0]['id']
    result1 = new_fv_article(id)
    result2 = new_comment(id)
    result3 = new_fv_cm(id)
    result4 = new_nested_cm(id)
    result5 = new_fv_nested_cm(id)
    return {"new_fv_article": result1,
            "new_comment": result2,
            "new_fv_cm": result3,
            "new_nested_cm": result4,
            "new_fv_nested_cm": result5}


def new_fv_article(id):
    state = f"""SELECT 
	id_user,
	id_article,
	id 
	FROM social_app.favorited_article WHERE social_app.favorited_article.id IN (SELECT 
										id_new_fv_ar 
			FROM social_app.notification WHERE id_user = '{id}')"""
    result = execute_sql(state)
    return result


def new_comment(id):
    state = f"""SELECT 
	id ,
	id_article,
	id_user ,
	body ,
	created_at
	FROM social_app.comments WHERE social_app.comments.id in (SELECT id_new_cm FROM social_app.notification WHERE id_user = '{id}')"""
    result = execute_sql(state)
    return result


def new_fv_cm(id):
    state = f"""SELECT 
	id_comment ,
	id_user 
	FROM social_app.favorited_comments WHERE social_app.favorited_comments.id 
    in (SELECT id_new_cm FROM social_app.notification WHERE id_user = '{id}') 
    """
    result = execute_sql(state)
    return result


def new_nested_cm(id):
    state = f"""SELECT 
	id,
	id_big,
	id_user,
	id_article,
	body,
	created_at 
	FROM social_app.nested_comment WHERE social_app.nested_comment.id IN (SELECT 
										id_new_nested_cm  
			FROM social_app.notification WHERE id_user = '{id}')"""
    result = execute_sql(state)
    return result


def new_fv_nested_cm(id):
    state = f"""SELECT 
	id_nested_comment,
	id_user,
	id 
	FROM social_app.favorited_nested_comments WHERE social_app.favorited_nested_comments.id IN (SELECT 
										id_new_fv_nested_cm  
			FROM social_app.notification WHERE id_user = '{id}') """
    result = execute_sql(state)
    return result


@user.route(Endpoint.USER3, methods=[HttpMethod.POST])
def add_new_message(id_user):
    token = request.headers.get("Authorization")
    if not token : 
        return jsonify({'message':'check your headers'})
    token = decode(token)
    username = token['username'] 
    if not username : 
        return jsonify({'message':'check your token'})
    state = f"""SELECT id FROM social_app.user WHERE username = '{username}'"""
    id = execute_sql(state)
    id = id[0]['id']
    data = request.get_json()
    data = data.get('message', {})
    body = data.get('body')
    date = datetime.now()
    state = f"""INSERT INTO social_app.message(id_author,id_user,created_at,body) VALUES('{id}','{id_user}','{date}','{body}')"""
    execute_sql1(state)
    state = f"""SELECT body FROM social_app.message WHERE id_author='{id}' AND id_user='{id_user}' AND created_at = '{date}'"""
    result = execute_sql(state)
    return result



@user.route(Endpoint.USER3, methods=[HttpMethod.GET])
def get_all_message(id_user):
    token = request.headers.get("Authorization")
    if not token : 
        return jsonify({'message':'check your headers'})
    token = decode(token)
    username = token['username'] 
    if not username : 
        return jsonify({'message':'check your token'})
    state = f"""SELECT id FROM social_app.user WHERE username = '{username}'"""
    id = execute_sql(state)
    id = id[0]['id']
    state = f"""SELECT * FROM social_app.message WHERE id_author ='{id}' AND id_user ='{id_user}'"""
    result = execute_sql(state)
    return {"message":result}
