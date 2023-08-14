from src.api import HttpMethod
from src.api.urls import Endpoint
from src.common.utils.alchemy import execute_sql, execute_sql1
from flask import Blueprint, request, jsonify
from datetime import datetime
from src.common.utils.social_jwt import decode, encode
article = Blueprint("article", __name__)


@article.route(Endpoint.ARTICLE, methods=[HttpMethod.GET])
def get_all_article():
    state = """SELECT
                    social_app.article.id,
                    social_app.article.title,
                    social_app.article.body,
                    social_app.article.created_at,
                    social_app.USER.name,
                    social_app.USER.bio,
                    social_app.USER.image,
                    COUNT ( social_app.favorited_article.id_article ) AS favorites_count 
                FROM
                    social_app.article
                    LEFT JOIN social_app.USER ON social_app.article.id_author = social_app.USER.
                    ID LEFT JOIN social_app.favorited_article ON social_app.article.id = social_app.favorited_article.id_article 
                GROUP BY
                    social_app.article.id,
                    social_app.article.title,
                    social_app.article.body,
                    social_app.article.created_at,
                    social_app.USER.name,
                    social_app.USER.bio,
                    social_app.USER.image"""

    result = execute_sql(state)
    author = {}
    for i in result:
        a = i['name']
        b = i['bio']
        c = i['image']
        del i['name']
        del i['bio']
        del i['image']
        author['name'] = a
        author['bio'] = b
        author['image'] = c
        i['author'] = author
        return {'articles': result,
                'article_count': len(result)
                }


@article.route(Endpoint.ARTICLE1, methods=[HttpMethod.GET])
def get_one_article(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if username:
        state = f"""SELECT
        article.ID,
        article.title,
        article.body,
        article.created_at,
        article.image,
        social_app.USER.NAME,
        social_app.USER.bio,
        social_app.USER.image,
        COUNT ( favorited_article.id_article ) AS favorites_count 
        FROM
            social_app.article AS article
            LEFT JOIN social_app.USER ON article.id_author = social_app.USER.id
            LEFT JOIN social_app.favorited_article ON favorited_article.id_article = article.ID 
        WHERE 
            article.id = ('{id_article}')
        GROUP BY
            article.ID,
            article.title,
            article.body,
            article.created_at,
            article.image,
            social_app.USER.NAME,
            social_app.USER.bio,
            social_app.USER.image"""
        result = execute_sql(state)
        result = result[0]
        author = {}
        author['name'] = result['name']
        author['bio'] = result['bio']
        author['image'] = result['image']
        result['author'] = author
        del result['bio']
        del result['name']
        del result['image']
        return {'article': result}


@article.route(Endpoint.COMMENTS, methods=[HttpMethod.GET])
def get_all_comments(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if username:
        state = f"""SELECT 
            comments.id,
            comments.body,
            comments.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.comments 
	    LEFT JOIN social_app.user ON comments.id_user = social_app.user.id 
	    LEFT JOIN social_app.article ON comments.id_article = social_app.article.id 
    WHERE 
	    social_app.article.id = ('{id_article}')
"""
        result = execute_sql(state)
        for i in result:
            name = i["name"]
            bio = i["bio"]
            image = i["image"]
            author = {}
            author["name"] = name
            author["bio"] = bio
            author["image"] = image
            del i["bio"]
            del i["name"]
            del i["image"]
            i["author"] = author
        return {"comments": result,
                }


@article.route(Endpoint.ARTICLE2, methods=[HttpMethod.POST])
def add_favorite_article(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT id_user FROM social_app.favorited_article WHERE id_article = ('{id_article}')"""
    result = execute_sql(state)
    if result:
        return unfavorite_article(id_article)
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""INSERT INTO social_app.favorited_article(id_user,id_article) VALUES('{id}','{id_article}')"""
    execute_sql1(state)
    result = get_one_article(id_article)
    return result


@article.route(Endpoint.ARTICLE2, methods=[HttpMethod.DELETE])
def unfavorite_article(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""DELETE FROM social_app.favorited_article WHERE id_user = ('{id}') AND id_article=('{id_article}') """
    execute_sql1(state)
    result = get_one_article(id_article)
    return result


@article.route(Endpoint.ARTICLE3, methods=[HttpMethod.POST])
def add_favorites_comments(id_comment):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT id_user FROM social_app.favorited_comments WHERE id_comment = ('{id_comment}')"""
    result = execute_sql(state)
    if result:
        return unfavorites_comments(id_comment)
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""INSERT INTO social_app.favorited_comments(id_user,id_comment) VALUES('{id}','{id_comment}')"""
    execute_sql1(state)
    state = f"""SELECT 
            comments.id,
            comments.body,
            comments.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.comments 
	    LEFT JOIN social_app.user ON comments.id_user = social_app.user.id 
    WHERE 
	    social_app.comments.id = ('{id_comment}')"""
    result = execute_sql(state)
    result = result[0]
    author = {}
    author['name'] = result['name']
    author['bio'] = result['bio']
    author['image'] = result['image']
    result['author'] = author
    del result['name']
    del result['bio']
    del result['image']
    return {'comment': result}


@article.route(Endpoint.ARTICLE3, methods=[HttpMethod.DELETE])
def unfavorites_comments(id_comment):

    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""DELETE FROM social_app.favorited_comments WHERE id_comment = ('{id_comment}')"""
    execute_sql1(state)
    state = f"""SELECT 
            comments.id,
            comments.body,
            comments.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.comments 
	    LEFT JOIN social_app.user ON comments.id_user = social_app.user.id 
    WHERE 
	    social_app.comments.id = ('{id_comment}')"""
    result = execute_sql(state)
    result = result[0]
    author = {}
    author['name'] = result['name']
    author['bio'] = result['bio']
    author['image'] = result['image']
    result['author'] = author
    del result['name']
    del result['bio']
    del result['image']
    return {'comment': result}


@article.route(Endpoint.ARTICLE4, methods=[HttpMethod.POST])
def add_favorite_nested_comment(id_nested_comment):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT id_user FROM social_app.favorited_comments WHERE id_comment = ('{id_nested_comment}')"""
    result = execute_sql(state)
    if result:
        return unfavorite_nested_comment(id_nested_comment)
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""INSERT INTO social_app.favorited_nested_comments(id_user,id_nested_comment) VALUES('{id}','{id_nested_comment}')"""
    execute_sql1(state)
    state = f"""SELECT 
            nested_comment.id,
            nested_comment.id_big,
            nested_comment.body,
            nested_comment.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.nested_comment
	    LEFT JOIN social_app.user ON nested_comment.id_user = social_app.user.id 
    WHERE 
	    social_app.nested_comment.id = ('{id_nested_comment}')"""
    result = execute_sql(state)
    result = result[0]
    author = {}
    author['name'] = result['name']
    author['bio'] = result['bio']
    author['image'] = result['image']
    result['author'] = author
    del result['name']
    del result['bio']
    del result['image']
    return {'nested_comment': result}


@article.route(Endpoint.ARTICLE4, methods=[HttpMethod.DELETE])
def unfavorite_nested_comment(id_nested_comment):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""DELETE FROM social_app.favorited_nested_comments WHERE id_nested_comment = ('{id_nested_comment}') AND id_user =('{id}')"""
    execute_sql1(state)
    state = f"""SELECT 
            nested_comment.id,
            nested_comment.id_big,
            nested_comment.body,
            nested_comment.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.nested_comment
	    LEFT JOIN social_app.user ON nested_comment.id_user = social_app.user.id 
    WHERE 
	    social_app.nested_comment.id = ('{id_nested_comment}')"""
    result = execute_sql(state)
    result = result[0]
    author = {}
    author['name'] = result['name']
    author['bio'] = result['bio']
    author['image'] = result['image']
    result['author'] = author
    del result['name']
    del result['bio']
    del result['image']
    return {'nested_comment': result}


@article.route(Endpoint.ARTICLE, methods=[HttpMethod.POST])
def add_article():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id_author = result[0]['id']
    data = request.get_json()
    data = data.get("article", {})
    title = data.get('title')
    body = data.get('body')
    image = data.get('image')
    created_at = datetime.now()
    state = f"""INSERT INTO social_app.article(title,body,image,created_at,id_author) VALUES('{title}','{body}','{image}','{created_at}','{id_author}')"""
    execute_sql1(state)
    state = f"SELECT social_app.article.id FROM social_app.article WHERE id_author = ('{id_author}') AND created_at =('{created_at}')"
    result = execute_sql(state)
    result = result[0]['id']
    result = get_one_article(result)
    return result


@article.route(Endpoint.ARTICLE5, methods=[HttpMethod.POST])
def add_comments(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id_author = result[0]['id']
    data = request.get_json()
    data = data.get('comment')
    body = data.get('body')
    date = datetime.now()
    state = f"""INSERT INTO social_app.comments(id_article,id_user,body,created_at) VALUES('{id_article}','{id_author}','{body}','{date}')"""
    execute_sql1(state)
    state = f"""SELECT id FROM social_app.comments WHERE id_user='{id_author}' AND created_at = '{date}'"""
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""SELECT 
            comments.id,
            comments.body,
            comments.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.comments 
	    LEFT JOIN social_app.user ON comments.id_user = social_app.user.id 
    WHERE 
	    social_app.comments.id = ('{id}')"""
    result = execute_sql(state)
    result = result[0]
    author = {}
    author['name'] = result['name']
    author['bio'] = result['bio']
    author['image'] = result['image']
    del result['name']
    del result['bio']
    del result['image']
    result['author'] = author

    return {'comment': result}
# check again how to connect with front end


@article.route(Endpoint.ARTICLE6, methods=[HttpMethod.POST])
def add_nested_comments(id_article, id_comment):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
    result = execute_sql(state)
    id_author = result[0]['id']
    data = request.get_json()
    data = data.get('nested_comment')
    body = data.get('body')
    date = datetime.now()
    state = f"""INSERT INTO social_app.nested_comment(id_big,id_user,id_article,body,created_at) VALUES('{id_comment}','{id_author}','{id_article}','{body}','{date}')"""
    execute_sql1(state)
    state = f"""SELECT id FROM social_app.nested_comment WHERE id_user='{id_author}' AND created_at = '{date}'"""
    result = execute_sql(state)
    id = result[0]['id']
    state = f"""SELECT 
            nested_comment.id,
            nested_comment.id_big,
            nested_comment.id_article,
            nested_comment.body,
            nested_comment.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
    FROM social_app.nested_comment
        LEFT JOIN social_app.user ON nested_comment.id_user = social_app.user.id 
    WHERE 
        social_app.nested_comment.id = ('{id}')"""
    result = execute_sql(state)
    result = result[0]
    author = {}
    author['name'] = result['name']
    author['bio'] = result['bio']
    author['image'] = result['image']
    del result['name']
    del result['bio']
    del result['image']
    result['author'] = author

    return {'comment': result}


@article.route(Endpoint.ARTICLE1, methods=[HttpMethod.DELETE])
def delete_article(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
    result = execute_sql(state)
    id = result[0]['id_author']
    state = f"""SELECT username FROM social_app.user WHERE social_app.user.id = ('{id}')"""
    result = execute_sql(state)
    result = result[0]['username']
    if username == result:
        state = f"""DELETE FROM social_app.article WHERE social_app.article.id='{id_article}'"""
        execute_sql1(state)
        return jsonify({'message': 'delete succesfully'})
    return jsonify({'message': 'you are not own this article'})


@article.route(Endpoint.ARTICLE1, methods=[HttpMethod.PUT])
def update_article(id_article):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state1 = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
    result1 = execute_sql(state1)
    id1 = result1[0]['id_author']
    state2 = f"""SELECT username FROM social_app.user WHERE social_app.user.id = ('{id1}')"""
    result2 = execute_sql(state2)
    result2 = result2[0]['username']
    if username == result2:
        data = request.get_json()
        data = data.get('article', {})
        title = data.get('title')
        body = data.get('body')
        image = data.get('image')
        state = f"""UPDATE social_app.article SET title='{title}',body='{body}',image='{image}' WHERE id='{id_article}'"""
        execute_sql1(state)
        result = get_one_article(id_article)
        return result
    return jsonify({'message': 'cannot update '})


@article.route(Endpoint.ARTICLE7, methods=[HttpMethod.DELETE])
def delete_comment(id_article, id_comment):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state1 = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
    result1 = execute_sql(state1)
    id1 = result1[0]['id_author']
    state2 = f"""SELECT username FROM social_app.user WHERE social_app.user.id = ('{id1}')"""
    result2 = execute_sql(state2)
    result2 = result2[0]['username']
    state3 = f"SELECT id_user FROM social_app.comments WHERE social_app.comments.id ='{id_comment}'"
    result3 = execute_sql(state3)
    result3 = result3[0]['id_user']
    state4 = f"""SELECT username FROM social_app.user WHERE social_app.user.id = ('{result3}')"""
    result4 = execute_sql(state4)
    result4 = result4[0]['username']
    if username == result2 or username == result4:
        state = f"""DELETE FROM social_app.comments WHERE social_app.comments.id = '{id_comment}'"""
        execute_sql1(state)
        return jsonify({'message': 'deleted comment'})
    return jsonify({'message': 'cannot delete comment'})


@article.route(Endpoint.ARTICLE8, methods=[HttpMethod.DELETE])
def delete_nested_comment(id_article, id_nested_comment):
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "check your token"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username:
        return jsonify({'message': 'check your token'})
    state1 = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
    result1 = execute_sql(state1)
    id1 = result1[0]['id_author']
    state2 = f"""SELECT username FROM social_app.user WHERE social_app.user.id = ('{id1}')"""
    result2 = execute_sql(state2)
    result2 = result2[0]['username']
    state3 = f"""SELECT id_user FROM social_app.nested_comment WHERE social_app.nested_comment.id = ('{id_nested_comment}')"""
    result3 = execute_sql(state3)
    result3 = result3[0]['id_user']
    state4 = f"""SELECT username FROM social_app.user WHERE social_app.user.id = ('{result3}')"""
    result4 = execute_sql(state4)
    result4 = result4[0]['username']
    if username == result4 or username == result2:
        state5 = f"""DELETE FROM social_app.nested_comment WHERE id='{id_nested_comment}'"""
        execute_sql1(state5)
        return jsonify({'message': 'delete successfully'})
    return jsonify({'message': 'cannot delete nested comment'})

