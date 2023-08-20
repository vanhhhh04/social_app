from flask import Blueprint, request, jsonify
from src.api.urls import Endpoint
from src.api import HttpMethod
from datetime import datetime
from src.common.utils.alchemy import execute_sql, execute_sql1
from src.common.utils.social_jwt import encode, decode
from src.api.user.services import UserServices
user = Blueprint("user", __name__)


@user.route(Endpoint.USER, methods=[HttpMethod.POST])
def sign_up():
    data = request.get_json()
    name = data.get("user", {}).get("name")
    username = data.get("user", {}).get("username")
    password = data.get("user", {}).get("password")
    user_service = UserServices()
    result = user_service.sign_up(name,username,password) 
    return result 

# ....
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








@user.route(Endpoint.USER, methods=[HttpMethod.GET])
def get_current_user():
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    user_service = UserServices()
    result = user_service.get_current_user(id_author,token)
    return result 


@user.route(Endpoint.USER, methods=[HttpMethod.PUT])
def update_user():
    token = request.headers.get("Authorization")
    user_service = UserServices()
    id_user = user_service.get_user_id_from_token(token)
    data = request.get_json()
    data = data.get('user', {})
    new_name = data.get('name')
    new_bio = data.get('bio')
    new_image = data.get('image')
    new_password = data.get('password')
    result = user_service.update_user(id_user,token,new_name,new_bio,new_image,new_password)
    return result 


@user.route(Endpoint.PROFILE, methods=[HttpMethod.GET])
def get_profile_current_user():
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    result = user_services.get_profile_current_user(id_author)
    return result 


@user.route(Endpoint.PROFILE1, methods=[HttpMethod.GET])
def get_profile_user_with_condition():
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    get_by_name = request.args.get('name')
    result = user_services.get_profile_user_with_condition(get_by_name)
    return result 


@user.route(Endpoint.USER2, methods=[HttpMethod.GET])
def get_notification():
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    result = user_services.get_notification(id)
    return result 



@user.route(Endpoint.USER3, methods=[HttpMethod.POST])
def add_new_message(id_user):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
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
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    state = f"""SELECT * FROM social_app.message WHERE id_author ='{id}' AND id_user ='{id_user}'"""
    result = execute_sql(state)
    return {"message":result}


