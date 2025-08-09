from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch('app.main.notion')
def test_list_databases(mock_notion):
    mock_notion.search.return_value = {'results': [{'id': 'db1', 'object': 'database'}]}
    r = client.get('/v1/databases')
    assert r.status_code == 200
    data = r.json()
    assert 'results' in data
    assert data['results'][0]['id'] == 'db1'

@patch('app.main.notion')
def test_list_database_rows(mock_notion):
    mock_notion.databases.query.return_value = {'results': [{'id': 'row1'}]}
    r = client.get('/v1/databases/db123/rows')
    assert r.status_code == 200
    data = r.json()
    assert 'results' in data
    assert data['results'][0]['id'] == 'row1'
