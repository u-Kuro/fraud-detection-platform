from dags.shared.repositories.postgres.postgres import sql_session

def test_sql_session_instance():
    from sqlalchemy.orm import sessionmaker
    assert isinstance(sql_session, sessionmaker)
