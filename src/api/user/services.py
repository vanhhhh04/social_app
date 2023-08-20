from src.common.utils.social_jwt import decode, encode
from src.common.utils.alchemy import execute_sql,execute_sql1
from flask import jsonify

class UserServices:
	# def login(self, username, password):
    # 	if self.check_username(username):
    #     	if self.check_password(username, password):
	# 			user_credentials = {"username": username}
	# 			token = encode(user_credentials)
	# 			state = f"""SELECT name, bio, image FROM social_app.user WHERE username = ('{username}')"""
	# 			result = execute_sql(state)
	# 			name = result[0]['name']
	# 			bio = result[0]['bio']
	# 			image = result[0]['image']
	# 			return {
	# 				"user": {
	# 					"name": f"{name}",
	# 					"token": f"{token}",
	# 					"username": f"{username}",
	# 					"password": f"{password}",
	# 					"bio": f"{bio}",
	# 					"image": f"{image}"
	# 				}
	# 			}
	# 		return jsonify({"message": "check your password again"})
	# 	return jsonify({"message": "user did not existed"})

	def get_user_id_from_token(self, token):
		if not token:
			raise Exception("Token is invalid")
		jwt_token = decode(token)
		username = jwt_token['username']
		state = f"SELECT id FROM social_app.user WHERE username=('{username}')"
		result = execute_sql(state)
		if len(result) == 0:
			raise Exception('User is not exist')
		id_author = result[0].get("id")
		if not id_author:
			raise Exception("User is not exist")
		return id_author
	
	def check_username(self,username):
		state = f"""SELECT username FROM social_app.user WHERE username = ('{username}')"""
		result = execute_sql(state)
		if result:
			return True
		else:
			return False

	def check_password(self,username, password):
		state = f"""SELECT password FROM social_app.user WHERE username = ('{username}')"""
		result = execute_sql(state)
		result = result[0]['password']
		if password == result:
			return True
		else:
			return False

	def sign_up(self,name,username,password):
		state = f"""INSERT INTO social_app.user(name,username,password) VALUES ('{name}','{username}','{password}')"""
		if self.check_username(username):
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


	def get_current_user(self,id_author,token):
		state = f"""SELECT * FROM social_app.user WHERE id =('{id_author}')"""
		result = execute_sql(state)
		name = result[0]['name']
		bio = result[0]['bio']
		image = result[0]['image']
		return {"user": {
				"name": f"{name}",
				"token": f"{token}",
				"bio": f"{bio}",
				"image": f"{image}"
				}
				}
	def update_user(self,id_user,token,new_name,new_bio,new_image,new_password):
		state = f"""SELECT * FROM social_app.user WHERE id =('{id_user}')"""
		result = execute_sql(state)
		name = result[0]['name']
		password = result[0]['password']
		if not new_name:
			if not new_password:
				state = f"""UPDATE social_app.user SET name =('{name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{password}') 
				WHERE id=('{id_user}')"""
				execute_sql1(state)
			else:
				state = f"""UPDATE social_app.user SET name =('{name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{new_password}') 
				WHERE id=('{id_user}')"""
				execute_sql1(state)
		else:
			state = f"""UPDATE social_app.user SET name =('{new_name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{new_password}') 
			WHERE id=('{id_user}')"""
			execute_sql1(state)
		if new_name:
			if not new_password:
				state = f"""UPDATE social_app.user SET name =('{new_name}'),bio =('{new_bio}'),image=('{new_image}'),password = ('{password}') 
				WHERE id=('{id_user}')"""
				execute_sql1(state)
		execute_sql1(state)
		result = self.get_current_user(id_user,token)
		return result
	
	def get_profile_current_user(self,id_author):
		state = f"""SELECT * FROM social_app.user WHERE id = ('{id_author}')"""
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



	def respond_para(get_by_name):
		state = f"SELECT name,id FROM social_app.user WHERE name='{get_by_name}' "
		result = execute_sql(state)
		dic = {}
		lit = []
		for i in result:
			if get_by_name in i['name']:
				dic[i['name']] = i['id']
		for j in dic.values():
			lit.append(j)
		return lit
	
	def get_profile_user_with_condition(self,get_by_name):
		result = self.respond_para(get_by_name)
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
		

		
	def new_fv_article(self,id):
		state = f"""SELECT 
		id_user,
		id_article,
		id 
		FROM social_app.favorited_article WHERE social_app.favorited_article.id IN (SELECT 
											id_new_fv_ar 
				FROM social_app.notification WHERE id_user = '{id}')"""
		result = execute_sql(state)
		return result

	def new_comment(self,id):
		state = f"""SELECT 
		id ,
		id_article,
		id_user ,
		body ,
		created_at
		FROM social_app.comments WHERE social_app.comments.id in (SELECT id_new_cm FROM social_app.notification WHERE id_user = '{id}')"""
		result = execute_sql(state)
		return result
	
	def new_fv_cm(self,id):
		state = f"""SELECT 
		id_comment ,
		id_user 
		FROM social_app.favorited_comments WHERE social_app.favorited_comments.id 
		in (SELECT id_new_cm FROM social_app.notification WHERE id_user = '{id}') 
		"""
		result = execute_sql(state)
		return result

	def new_nested_cm(self,id):
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
	
	def new_fv_nested_cm(self,id):
		state = f"""SELECT 
		id_nested_comment,
		id_user,
		id 
		FROM social_app.favorited_nested_comments WHERE social_app.favorited_nested_comments.id IN (SELECT 
											id_new_fv_nested_cm  
				FROM social_app.notification WHERE id_user = '{id}') """
		result = execute_sql(state)
		return result

	def get_notification(self,id):
		result1 = self.new_fv_article(id)
		result2 = self.new_comment(id)
		result3 = self.new_fv_cm(id)
		result4 = self.new_nested_cm(id)
		result5 = self.new_fv_nested_cm(id)
		return {"new_fv_article": result1,
				"new_comment": result2,
				"new_fv_cm": result3,
				"new_nested_cm": result4,
				"new_fv_nested_cm": result5}
