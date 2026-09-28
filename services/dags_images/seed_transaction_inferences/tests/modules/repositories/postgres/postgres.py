from sqlalchemy.orm import sessionmaker

from seed_transaction_inferences.repositories.postgres.postgres import sql_session

def test_sql_session_instance():
    assert isinstance(sql_session, sessionmaker)