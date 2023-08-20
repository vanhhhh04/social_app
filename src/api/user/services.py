from src.common.utils.social_jwt import decode, encode
from src.common.utils.alchemy import execute_sql


class UserServices:
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