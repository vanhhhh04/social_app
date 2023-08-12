from flask import Blueprint,request,jsonify
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql,execute_sql1
from src.common.utils.social_jwt import encode,decode
user = Blueprint("user",__name__)



@user.route(Endpoint.USER, methods=[HttpMethod.POST])
def sign_up() :
    data = request.get_json()
    name = data.get("user", {}).get("name")
    username = data.get("user", {}).get("username")
    password = data.get("user",{}).get("password")
    state =f"""INSERT INTO social_app.user(name,username,password) VALUES ('{name}','{username}','{password}')"""
    if check_username(username) :
        return jsonify({"message":"username was existed"})
    else :
        execute_sql1(state)
        return {"user":{
                "name" : f"{name}",
                "username" : f"{username}",
                "password" : f"{password}",
                "bio" : None ,
                "image" : None,
                }
                }


def check_username(username) :
    state = f"""SELECT username FROM social_app.user WHERE username = ('{username}')"""
    result = execute_sql(state) 
    if result : 
        return True 
    else : 
        return False 



@user.route(Endpoint.USER1, methods=[HttpMethod.POST])
def login():
    data = request.get_json()
    data = data.get("user",{})
    username = data.get("username") 
    password = data.get("password")
    user_credentials = {"username":username}
    if check_username(username):
        if check_password(username,password) :
            token = encode(user_credentials) 
            state = f"""SELECT name,bio,image FROM social_app.user WHERE username =('{username}')"""
            result = execute_sql(state)
            name = result[0]['name']
            bio = result[0]['bio']
            image = result[0]['image']
            return {"user" : {
                    "name" :f"{name}",
                    "token":f"{token}" ,
                    "username":f"{username}",
                    "password":f"{password}",
                    "bio" :f"{bio}",
                    "image":f"{image}"
                            }
                    }
        else :
            return jsonify({"message":"check your password again"})
    else : 
        return jsonify({"message":"user did not existed"})


def check_username(username):
    state = f"""SELECT username FROM social_app.user WHERE username = ('{username}')"""
    result = execute_sql(state) 
    if result :
        return True 
    else :
        return False 


def check_password(username,password):
    state =f"""SELECT password FROM social_app.user WHERE username = ('{username}')"""
    result = execute_sql(state) 
    result = result[0]['password']
    if password == result :
        return True 
    else : 
        return False 


@user.route(Endpoint.USER, methods=[HttpMethod.GET]) 
def get_current_user():
    token = request.headers.get("Authorization")
    if not token :
        return jsonify({"message":"check your token"})
    jwt_token = decode(token) 
    username = jwt_token['username']
    if username : 
        state = f"""SELECT * FROM social_app.user WHERE username =('{username}')"""
        result = execute_sql(state)
        name = result[0]['name']
        password = result[0]['password']
        bio = result[0]['bio']
        image = result[0]['image']
        return {"user" : {
                "name" :f"{name}",
                "token":f"{token}" ,
                "username":f"{username}",
                "password":f"{password}",
                "bio" :f"{bio}",
                "image":f"{image}"
                        }
                }
    return jsonify({"message":"check your token"})


@user.route(Endpoint.USER, methods=[HttpMethod.PUT])
def update_user():
    token = request.headers.get("Authorization")
    if not token :
        return jsonify({"message":"check your token"})
    jwt_token = decode(token) 
    username = jwt_token['username']
    if not username : 
        return jsonify({'message':'check your token'})
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
    if not new_name : 
        if not new_password:
            #  khong khong 
            state = f"""UPDATE social_app.user SET name =('{name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{password}') 
            WHERE username=('{username}')"""
            execute_sql1(state)
        # khong co 
        else :
            state = f"""UPDATE social_app.user SET name =('{name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{new_password}') 
            WHERE username=('{username}')"""
            execute_sql1(state)
    # co co 
    else :
        state = f"""UPDATE social_app.user SET name =('{new_name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{new_password}') 
        WHERE username=('{username}')"""
        execute_sql1(state)
    # co khong
    if new_name :
        if not new_password : 
            state = f"""UPDATE social_app.user SET name =('{new_name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{password}') 
            WHERE username=('{username}')"""
            execute_sql1(state)
    execute_sql1(state)
    result = get_current_user()
    return result 



@user.route(Endpoint.PROFILE, methods=[HttpMethod.GET])
def get_profile_current_user():
    token = request.headers.get("Authorization")
    if not token :
        return jsonify({"message":"check your token"})
    jwt_token = decode(token) 
    username = jwt_token['username']
    if not username : 
        return jsonify({'message':'check your token'})
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
            article.id = ('{id}')
        GROUP BY
            article.ID,
            article.title,
            article.body,
            article.created_at"""
    
    result = execute_sql(state)
    return {"profile" :result1,
        "articles":result}

     



