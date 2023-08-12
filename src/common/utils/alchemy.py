from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/postgres")


def execute_sql1(state):
    with engine.connect() as con:
        statement = text(f"{state}")
        con.execute(statement)
        con.commit()
        return True


def execute_sql(state):
    with engine.connect() as con:
        statement = text(f"{state}")
        result = con.execute(statement)
        first = result.fetchall()
        list_data = []
        for i in first:
            list_data.append(dict(i._mapping))
        return list_data
if __name__=="__main__" :
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
    print(result)