from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch('app.main.notion')
def test_get_page(mock_notion):
    mock_notion.pages.retrieve.return_value = {'id': 'page1', 'object': 'page'}
    mock_notion.blocks.children.list.return_value = {'results': []}
    r = client.get('/v1/pages/page1')
    assert r.status_code == 200
    data = r.json()
    assert 'page' in data
    assert data['page']['id'] == 'page1'

@patch('app.main.notion')
def test_create_page(mock_notion):
    mock_notion.pages.create.return_value = {'id': 'newpage'}
    payload = {
        'parent_database_id': 'db1',
        'properties': {'Name': {'title': [{'text': {'content': 'Hello'}}]}},
        'children': []
    }
    r = client.post('/v1/pages', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data['id'] == 'newpage'

@patch('app.main.notion')
def test_update_page(mock_notion):
    mock_notion.pages.update.return_value = {'id': 'page1'}
    payload = {'properties': {'Name': {'title': [{'text': {'content': 'Updated'}}]}}}
    r = client.patch('/v1/pages/page1', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data['id'] == 'page1'
