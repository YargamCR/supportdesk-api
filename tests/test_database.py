from unittest.mock import Mock

from app.db import database


def test_get_db_closes_session(monkeypatch):
    mock_session = Mock()

    monkeypatch.setattr(database, "SessionLocal", lambda: mock_session)

    db_generator = database.get_db()

    assert next(db_generator) is mock_session

    db_generator.close()

    mock_session.close.assert_called_once()
