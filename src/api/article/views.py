from src.api import HttpMethod
from src.api.urls import Endpoint
from src.common.utils.alchemy import execute_sql, execute_sql1
from flask import Blueprint, request, jsonify
from datetime import datetime
from src.common.utils.social_jwt import decode, encode
from src.api.article.services import ArticleServices
from src.api.user.services import UserServices
from src.api.article.services import ArticleServices,CommentServices
article = Blueprint("article", __name__)

@article.route(Endpoint.ARTICLE, methods=[HttpMethod.POST])
def create_article():
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    data = request.get_json()
    data = data.get("article", {})
    title = data.get('title')
    body = data.get('body')
    image = data.get('image')
    created_at = datetime.now()
    article_service =  ArticleServices()
    id_article = article_service.create_article(title,body,image,id_author,created_at)
    result = get_one_article(id_article)
    return result

@article.route(Endpoint.ARTICLE1, methods=[HttpMethod.DELETE])
def delete_article(id_article):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_user = user_services.get_user_id_from_token(token)
    article_service = ArticleServices()
    result = article_service.delete_article(id_user,id_article)
    return jsonify({'message': 'delete succesfully'})


@article.route(Endpoint.ARTICLE1, methods=[HttpMethod.PUT])
def update_article(id_article):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_user = user_services.get_user_id_from_token(token)
    data = request.get_json()
    data = data.get('article', {})
    title = data.get('title')
    body = data.get('body')
    image = data.get('image')
    article_service = ArticleServices()
    result = article_service.update_article(id_user,id_article,title,body,image)
    return jsonify({'message': 'update_succesfully '})

@article.route(Endpoint.ARTICLE, methods=[HttpMethod.GET])
def get_all_article():
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    article_service = ArticleServices()
    result = article_service.get_all_article()
    return {'articles': result,
            'article_count': len(result)
            }


@article.route(Endpoint.ARTICLE1, methods=[HttpMethod.GET])
def get_one_article(id_article):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    if id_author:
        article_service = ArticleServices()
        result = article_service.get_one_article(id_article)
        return {'article': result}


@article.route(Endpoint.COMMENTS, methods=[HttpMethod.GET])
def get_all_comments(id_article):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token)
    if id_author :
        article_service = ArticleServices()
        result = article_service.get_all_comments(id_article)
        return {"comments": result
                }


@article.route(Endpoint.ARTICLE2, methods=[HttpMethod.POST])
def add_favorite_article(id_article):
    token = request.headers.get("Authorization")
    user_service = UserServices()
    id = user_service.get_user_id_from_token(token)
    article_servicer = ArticleServices()
    result = article_servicer.add_favorite_article(id,id_article)
    return result


@article.route(Endpoint.ARTICLE2, methods=[HttpMethod.DELETE])
def unfavorite_article(id_article):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    article_service = ArticleServices()
    result = article_service.unfavorite_article(id,id_article)    
    return result


@article.route(Endpoint.ARTICLE3, methods=[HttpMethod.POST])
def add_favorites_comments(id_comment):
    token = request.headers.get("Authorization")
    user_service = UserServices()
    id = user_service.get_user_id_from_token(token)
    comment_service = CommentServices
    result = comment_service.add_favorites_comments(id,id_comment)
    return {'comment': result}


@article.route(Endpoint.ARTICLE3, methods=[HttpMethod.DELETE])
def unfavorites_comments(id_comment):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    comment_service =  CommentServices()
    result = comment_service.unfavorites_comments(id,id_comment)
    return {'comment': result}


@article.route(Endpoint.ARTICLE4, methods=[HttpMethod.POST])
def add_favorite_nested_comment(id_nested_comment):
    token = request.headers.get("Authorization")
    user_service = UserServices()
    id = user_service.get_user_id_from_token(token)
    comment_service = CommentServices()
    result = comment_service.add_favorite_nested_comment(id,id_nested_comment)
    return {'nested_comment': result}

@article.route(Endpoint.ARTICLE4, methods=[HttpMethod.DELETE])
def unfavorite_nested_comment(id_nested_comment):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    comment_service = CommentServices()
    result = comment_service.add_favorite_nested_comment(id,id_nested_comment)
    return {'nested_comment': result}



@article.route(Endpoint.ARTICLE5, methods=[HttpMethod.POST])
def add_comments(id_article):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    data = request.get_json()
    data = data.get('comment')
    body = data.get('body')
    comment_service = CommentServices()
    result = comment_service.add_comment(id,id_article,body)
    return {'comment': result}


@article.route(Endpoint.ARTICLE6, methods=[HttpMethod.POST])
def add_nested_comments(id_article,id_comment):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id = user_services.get_user_id_from_token(token)
    data = request.get_json()
    data = data.get('nested_comment')
    body = data.get('body')
    comment_service = CommentServices()
    result = comment_service.add_nested_comments(id,id_article,id_comment,body)
    return {'nested_comment': result}


@article.route(Endpoint.ARTICLE6, methods=[HttpMethod.GET])
def get_all_nested_cm_in_one_cm(id_article, id_comment):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_author = user_services.get_user_id_from_token(token) 
    comment_service = CommentServices()
    result = comment_service.get_all_nested_cm_in_one_cm(id_article,id_comment)
    return{"nested_comment":result}


@article.route(Endpoint.ARTICLE7, methods=[HttpMethod.DELETE])
def delete_comment(id_article, id_comment):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_user = user_services.get_user_id_from_token(token)
    comment_service = CommentServices()
    result = comment_service.delete_comment(id_user,id_article,id_comment)
    return result 


@article.route(Endpoint.ARTICLE8, methods=[HttpMethod.DELETE])
def delete_nested_comment(id_article, id_nested_comment):
    token = request.headers.get("Authorization")
    user_services = UserServices()
    id_user = user_services.get_user_id_from_token(token)
    comment_service = CommentServices()
    result = comment_service.delete_nested_comment(id_user,id_article,id_nested_comment)
    return jsonify({'message': 'cannot delete nested comment'})








