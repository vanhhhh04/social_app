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
    state = "SELECT name,id FROM social_app.user "
    result = execute_sql(state)
    for i in result :
        print(i)