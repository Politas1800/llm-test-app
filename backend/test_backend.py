import uuid
import pytest
from backend.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(scope="module")
def test_user():
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    response = client.post('/register', json={'username': unique_username, 'email': f'{unique_username}@example.com', 'password': 'testpassword'})
    assert response.status_code == 200, f'Expected 200, got {response.status_code}: {response.text}'
    print('Create user test passed')
    return unique_username

@pytest.fixture(scope="module")
def auth_token(test_user):
    response = client.post('/token', data={'username': test_user, 'password': 'testpassword'})
    assert response.status_code == 200, f'Expected 200, got {response.status_code}: {response.text}'
    print('Login test passed')
    return response.json()['access_token']

def test_create_test(auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    test_data = {
        'title': 'Test LLM',
        'description': 'A test for LLM',
        'user_message': 'Hello, LLM!',
        'review_message': 'Review this response',
        'num_requests': 1,
        'selected_llms': ['claude-3-opus-20240229'],
        'status': 'pending'  # Add this line
    }
    response = client.post('/tests', json=test_data, headers=headers)
    assert response.status_code == 200, f'Expected 200, got {response.status_code}: {response.text}'
    print('Create test passed')

def test_get_tests(auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/tests', headers=headers)
    assert response.status_code == 200, f'Expected 200, got {response.status_code}: {response.text}'
    print('Get tests passed')

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
