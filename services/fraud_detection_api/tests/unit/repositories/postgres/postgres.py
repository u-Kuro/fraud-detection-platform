from sqlalchemy.orm import sessionmaker

from fraud_detection_api.src.repositories.postgres.postgres import sql_session

def test_sql_session_instance():
    assert isinstance(sql_session, sessionmaker)