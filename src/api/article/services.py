from src.common.utils.alchemy import execute_sql,execute_sql1
from datetime import datetime
from flask import jsonify
class ArticleServices:
    def create_article(self, title, body, image, id_author,created_at):
        state = f"""INSERT INTO social_app.article(title,body,image,created_at,id_author) VALUES('{title}','{body}','{image}','{created_at}','{id_author}')"""
        execute_sql1(state)
        state = f"SELECT social_app.article.id FROM social_app.article WHERE id_author = ('{id_author}') AND created_at =('{created_at}')"
        result = execute_sql(state)
        id_article = result[0]['id']
        return id_article 
    
    def authen_owner_article(self,id_user,id_article):
        state = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
        result = execute_sql(state)
        id_author = result[0]['id_author']
        if id_user == id_author:
            return True
        raise Exception("you are not owner this article")
    
    
    def delete_article(self,id_user,id_article):
        self.authen_owner_article(id_user,id_article)
        # delete notification fv_new_article and fv_article  
        state = f"""SELECT id FROM social_app.favorited_article WHERE social_app.favorited_article.id_article='{id_article}'"""
        result = execute_sql(state)
        ds = []
        for i in result :
            for j in i.values():
                ds.append(j) 
        # in here ds is a list of favortie article 
        for t in ds : 
            state = f"""DELETE FROM social_app.notification WHERE social_app.notification.id_new_fv_ar='{t}'"""
            execute_sql1(state)
            state = f"""DELETE FROM social_app.favorited_article WHERE social_app.favorited_article.id_article ='{t}'"""
            execute_sql1(state)
        #  delete notification fv_new_nested_cm  
        state = f"""SELECT id FROM social_app.comments WHERE social_app.comments.id_article ='{id_article}'"""
        result = execute_sql(state)
    
        ds1 = [] 
        for i in result : 
            for j in i.values():
                ds1.append(j)
        # in here ds1 is a list of commnet into article 
        
        state = f"""SELECT id FROM social_app.nested_comment WHERE social_app.nested_comment.id_big IN (SELECT id FROM social_app.comments WHERE social_app.comments.id_article ='{id_article}')"""
        result = execute_sql(state)
        ds2 = []
        for i in result :
            for j in i.values():
                ds2.append(j) 
        # in here ds2 is a list of nested comment into a comment into a article which we want to delete
        # delete in notification id_new_nested_cm id_new_fv_nested_cm and in nested comment
        for t in ds2 :
            state = f"""DELETE FROM social_app.notification WHERE social_app.notification.id_new_nested_cm ='{t}'"""
            execute_sql1(state)
        for t in ds2:    
            state = f"""SELECT id FROM social_app.favorited_nested_comments WHERE id_nested_comment = '{t}'"""
            result = execute_sql(state)
            ds3 = []
            for i in result :
                for j in i.values():
                    ds3.append(j)
            # in here ds3 is a list of favorited nested cm 
            for h in ds3 :
                state = f"""DELETE FROM social_app.notification WHERE id_new_fv_nested_cm = '{h}'"""
                execute_sql1(state)
                state = f"""DELETE FROM social_app.favorited_nested_comments WHERE id = '{h}'"""
                execute_sql1(state)
            state = f"""DELETE FROM social_app.nested_comment WHERE id ='{t}'"""
            execute_sql1(state)
        #  delete column comment 
        for j in ds1 : 
            state = f"DELETE FROM social_app.notification WHERE social_app.notification.id_new_cm = '{j}'"
            execute_sql1(state)
            state =f"""SELECT id FROM social_app.favorited_comments WHERE social_app.favorited_comments.id_comment ='{j}'"""
            result = execute_sql(state)
            ds4 = []
            for i in result :
                for j in i.values() : 
                    ds3.append(j)
            # ds4 is a list of favorited comment 
            for t in ds4 :
                state = f"""DELETE FROM social_app.notification WHERE social_app.notification.id_new_fv_cm = '{t}'"""
                execute_sql1(state)
                state =f"""DELETE FROM social_app.favorited_comments WHERE social_app.favorited_comments.id ='{t}'"""
                execute_sql1(state)
        for j in ds1 :
            state =f"""DELETE FROM social_app.comments WHERE social_app.comments.id = '{j}'"""
            execute_sql1(state)
        state = f"""DELETE FROM social_app.article WHERE social_app.article ='{id_article}'"""
        execute_sql1(state)
    

    def update_article(self,id_user,id_article,title,body,image):
        self.authen_owner_article(id_user,id_article)
        state = f"""UPDATE social_app.article SET title='{title}',body='{body}',image='{image}' WHERE id='{id_article}'"""
        execute_sql1(state)
        result = self.get_one_article(id_article)
        return result


    def get_one_article(self,id_article):
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
        return result
    

    def get_all_article(self):
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
        return result 


    def get_all_comments(self,id_article):
        state = f"""SELECT 
            comments.id,
            comments.body,
            comments.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image,
						COUNT(favorited_comments.id) AS favorites_count
        FROM social_app.comments 
	    LEFT JOIN social_app.user ON comments.id_user = social_app.user.id 
	    LEFT JOIN social_app.article ON comments.id_article = social_app.article.id 
		LEFT JOIN social_app.favorited_comments ON social_app.favorited_comments.id_comment = social_app.comments.id 
        WHERE 
	    social_app.article.id = ('{id_article}') 
		GROUP BY 
						comments.id,
            comments.body,
            comments.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image
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
        return result 
    
 
    def add_favorite_article(self,id,id_article):
        state = f"""SELECT id_user FROM social_app.favorited_article WHERE id_article = ('{id_article}')"""
        result = execute_sql(state)
        lst = []
        for i in result :
            for j in i.values():
                lst.append(j)
        if id in lst : 
            return self.unfavorite_article(id,id_article)
        state = f"""INSERT INTO social_app.favorited_article(id_user,id_article) VALUES('{id}','{id_article}')"""
        execute_sql1(state)
        state = f"""SELECT id FROM social_app.favorited_article WHERE id_user ='{id}' AND id_article = '{id_article}'"""
        result = execute_sql(state)
        id_fv_ar = result[0]['id'] 
        state = f"""SELECT id_author FROM social_app.article LEFT JOIN social_app.favorited_article ON social_app.favorited_article.id_article 
            = social_app.article.id 
            WHERE social_app.favorited_article.id = '{id_fv_ar}'"""
        id_user = execute_sql(state)
        id_user = id_user[0]['id_author']
        date = datetime.now()
        state = f"""INSERT INTO social_app.notification(id_user,id_new_fv_ar,created_at) VALUES('{id_user}','{id_fv_ar}','{date}')"""
        execute_sql1(state)
        result = self.get_one_article(id_article)
        return result 
    
    
    def unfavorite_article(self,id,id_article):
        state1 = f"""SELECT id FROM social_app.favorited_article WHERE id_user = ('{id}') AND id_article=('{id_article}')"""
        result = execute_sql(state1)
        result = result[0]['id']
        state = f"""DELETE FROM social_app.notification WHERE id_new_fv_ar ='{result}'"""
        execute_sql1(state)
        state = f"""DELETE FROM social_app.favorited_article WHERE id_user = ('{id}') AND id_article=('{id_article}') """
        execute_sql1(state)
        result = self.get_one_article(id_article)
        return result 
    

    


class CommentServices:
    def get_single_comment(self,id_comment):
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
        return result 
    
    def add_favorites_comments(self,id,id_comment):
        state = f"""SELECT id_user FROM social_app.favorited_comments WHERE id_comment = ('{id_comment}')"""
        result = execute_sql(state)
        lst = []
        for i in result :
            for j in i.values():
                lst.append(j)
        if id in lst : 
            return self.unfavorites_comments(id,id_comment)
        state = f"""INSERT INTO social_app.favorited_comments(id_user,id_comment) VALUES('{id}','{id_comment}')"""
        execute_sql1(state)
        state = f"""SELECT id FROM social_app.favorited_comments WHERE id_user = '{id}' AND id_comment = '{id_comment}'"""
        result = execute_sql(state)
        id_new_fv_cm = result[0]['id']
        state = f"""SELECT
                social_app.article.id_author 
                FROM
                social_app.article
                LEFT JOIN social_app.comments ON social_app.comments.id_article = social_app.article.id 
                LEFT JOIN social_app.favorited_comments ON social_app.favorited_comments.id_comment = social_app.comments.id 
                WHERE
                social_app.favorited_comments.ID = '{id_new_fv_cm}'
                """
        id_user = execute_sql(state)
        id_user = id_user[0]['id_author']
        date = datetime.now()
        state = f"""INSERT INTO social_app.notification(id_user,id_new_fv_cm,created_at) VALUES('{id_user}','{id_new_fv_cm}','{date}')"""
        execute_sql1(state)
        result = self.get_single_comment(id_comment)
        return result 

    def unfavorites_comments(self,id,id_comment):
        state1 = f"""SELECT id FROM social_app.favorited_comments WHERE id_user='{id}' AND id_comment='{id_comment}'"""
        result = execute_sql(state1)
        id_fv_cm = result[0]['id']
        state = f"""DELETE FROM social_app.notification WHERE id_new_fv_cm ='{id_fv_cm}'"""
        execute_sql1(state)
        state = f"""DELETE FROM social_app.favorited_comments WHERE id_comment = ('{id_comment}') AND id_user = '{id}'"""
        execute_sql1(state)
        result = self.get_single_comment(id_comment)
        return result 
    
    def get_single_nested_comment(self,id_nested_comment):
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
        return result 

    def add_favorite_nested_comment(self,id,id_nested_comment):
        state = f"""SELECT id_user FROM social_app.favorited_nested_comments WHERE id_nested_comment = ('{id_nested_comment}')"""
        result = execute_sql(state)
        lst = []
        for i in result :
            for j in i.values():
                lst.append(j)
        if id in lst : 
            return self.unfavorite_nested_comment(id,id_nested_comment)
        state = f"""INSERT INTO social_app.favorited_nested_comments(id_user,id_nested_comment) VALUES('{id}','{id_nested_comment}')"""
        execute_sql1(state)
        state = f"""SELECT id FROM social_app.favorited_nested_comments WHERE id_user='{id}' AND id_nested_comment='{id_nested_comment}'"""
        result = execute_sql(state)
        id_fv_nested_cm = result[0]['id']
        state = f"""SELECT
                        a.id_author
                    FROM
                        social_app.article a
                        LEFT JOIN social_app.comments c ON c.id_article = a.id
                        LEFT JOIN social_app.nested_comment nc ON nc.id_big = c.id
                        LEFT JOIN social_app.favorited_nested_comments fnc ON fnc.id_nested_comment = nc.id
                    WHERE
                        fnc.ID = '{id_fv_nested_cm}';"""
        id_user = execute_sql(state)
        id_user = id_user[0]['id_author']
        date = datetime.now()
        state = f"""INSERT INTO social_app.notification(id_user,id_new_fv_nested_cm,created_at) VALUES('{id_user}','{id_fv_nested_cm}','{date}')"""
        execute_sql1(state)
        result = self.get_single_nested_comment(id_nested_comment)
        return result 

    def unfavorite_nested_comment(self,id,id_nested_comment):
        state1 = f"""SELECT id FROM social_app.favorited_nested_comments WHERE id_nested_comment ='{id_nested_comment}' AND id_user='{id}'"""
        result = execute_sql(state1)
        id_fv_nested_cm = result[0]['id']
        state2 = f"""DELETE FROM social_app.notification WHERE id_new_fv_nested_cm ='{id_fv_nested_cm}'"""
        execute_sql1(state2)
        state = f"""DELETE FROM social_app.favorited_nested_comments WHERE id_nested_comment = ('{id_nested_comment}') AND id_user =('{id}')"""
        execute_sql1(state)
        result = self.get_single_nested_comment(id_nested_comment)
        return result 

    def add_comment(self,id,id_article,body):
        date = datetime.now()
        state = f"""INSERT INTO social_app.comments(id_article,id_user,body,created_at) VALUES('{id_article}','{id}','{body}','{date}')"""
        execute_sql1(state)
        state = f"""SELECT id FROM social_app.comments WHERE id_user='{id}' AND created_at = '{date}'"""
        result = execute_sql(state)
        id_comment = result[0]['id']
        state = f"""SELECT id_author FROM social_app.article LEFT JOIN social_app.comments ON social_app.comments.id_article 
        = social_app.article.id WHERE social_app.comments.id = '{id}' """
        id_user = execute_sql(state)
        id_user = id_user[0]['id_author']
        date = datetime.now()
        state1 = f"""INSERT INTO social_app.notification(id_user,id_new_cm,created_at) VALUES ('{id_user}','{id}','{date}')"""
        execute_sql1(state1)
        result = self.get_single_comment(id_comment)
        return result 

    def add_nested_comments(self,id,id_article,id_comment,body):
        date = datetime.now()
        state = f"""INSERT INTO social_app.nested_comment(id_big,id_user,id_article,body,created_at) VALUES('{id_comment}','{id}','{id_article}','{body}','{date}')"""
        execute_sql1(state)
        state = f"""SELECT id FROM social_app.nested_comment WHERE id_user='{id}' AND created_at = '{date}'"""
        result = execute_sql(state)
        id_nested_comment = result[0]['id']
        state = f"""SELECT id_author FROM social_app.article LEFT JOIN social_app.comments ON social_app.comments.id_article 
        = social_app.article.id 
        LEFT JOIN social_app.nested_comment ON social_app.nested_comment.id_big = social_app.comments.id WHERE social_app.nested_comment.id = '{id}' """
        id_user = execute_sql(state)
        id_user = id_user[0]['id_author']
        date = datetime.now()
        state1 = f"""INSERT INTO social_app.notification(id_user,id_new_nested_cm,created_at) VALUES ('{id_user}','{id_nested_comment}','{date}')"""
        execute_sql1(state1)
        result = self.get_single_nested_comment(id_nested_comment)
        return result 
    
    def get_all_nested_cm_in_one_cm(self,id_article,id_comment):
        state = f"""SELECT 
            nested_comment.id,
            nested_comment.id_big,
            nested_comment.id_article,
            nested_comment.body,
            nested_comment.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image,
						COUNT(favorited_nested_comments.id) AS favorites_count
    FROM social_app.nested_comment
        LEFT JOIN social_app.user ON nested_comment.id_user = social_app.user.id 
				LEFT JOIN social_app.favorited_nested_comments ON social_app.favorited_nested_comments.id_nested_comment = social_app.nested_comment.id
    WHERE 
        social_app.nested_comment.id_big = ('{id_comment}') AND social_app.nested_comment.id_article='{id_article}'
		GROUP BY 
			nested_comment.id,
            nested_comment.id_big,
            nested_comment.id_article,
            nested_comment.body,
            nested_comment.created_at,
            social_app.user.name,
            social_app.user.bio,
            social_app.user.image """
        result = execute_sql(state)
        for i in result : 
            author = {}
            author['name'] = i['name']
            author['bio'] = i['bio']
            author['image'] = i['image']
            del i['name']
            del i['bio']
            del i['image']
            i['author'] = author
        return result 
    
    def delete_comment(self,id_user,id_article,id_comment):
        state1 = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
        result1 = execute_sql(state1)
        id1 = result1[0]['id_author']
        state3 = f"SELECT id_user FROM social_app.comments WHERE social_app.comments.id ='{id_comment}'"
        result3 = execute_sql(state3)
        result3 = result3[0]['id_user']
        if id_user == id1 or id_user == result3:
            state = f"""DELETE FROM social_app.notification WHERE id_new_cm ='{id_comment}'"""
            execute_sql1(state)
            state = f"""SELECT id FROM social_app.nested_comment WHERE social_app.nested_comment.id_big ='{id_comment}'"""
            result = execute_sql(state)
            ds = [] 
            for i in result : 
                for j in i.values():
                    ds.append(j)
            for t in ds : 
                state = f"""DELETE FROM social_app.favorited_nested_comments WHERE id_nested_comment = '{t}'"""
                execute_sql1(state)
            for t in ds : 
                state = f"""DELETE FROM social_app.nested_comment WHERE id = '{t}'"""
                execute_sql1(state)
            state = f"""DELETE FROM social_app.favorited_comments WHERE id_comment = '{id_comment}'"""
            execute_sql1(state)
            state = f"""DELETE FROM social_app.comments WHERE social_app.comments.id = '{id_comment}'"""
            execute_sql1(state)
            return jsonify({"message":"delete comment succesfully"})
        raise Exception("you cannot delete comment")
   
    def delete_nested_comment(self,id_user,id_article,id_nested_comment):
        state1 = f"""SELECT id_author FROM social_app.article WHERE social_app.article.id=('{id_article}')"""
        result1 = execute_sql(state1)
        id1 = result1[0]['id_author']
        state3 = f"""SELECT id_user FROM social_app.nested_comment WHERE social_app.nested_comment.id = ('{id_nested_comment}')"""
        result3 = execute_sql(state3)
        result3 = result3[0]['id_user']
        if id1 == id_user or id_user == result3:
            state = f"""DELETE FROM social_app.notification WHERE id_new_nested_cm = '{id_nested_comment}'"""
            execute_sql1(state)
            state = f"""DELETE FROM social_app.favorited_nested_comments WHERE id_nested_comment = '{id_nested_comment}'"""
            execute_sql1(state)
            state5 = f"""DELETE FROM social_app.nested_comment WHERE id='{id_nested_comment}'"""
            execute_sql1(state5)
            return jsonify({'message': 'delete successfully'})
        raise Exception("you cannot delete this comment")