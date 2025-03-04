import pytest
from unittest.mock import patch
from main import app
from forms import IngredientForm

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost'
    
    # Push an application context
    with app.app_context():
        # Create a test client
        with app.test_client() as testing_client:
            yield testing_client

@pytest.fixture
def mock_spoonacular_response():
    return [{
        "id": 123,
        "title": "Test Recipe",
        "image": "test.jpg",
        "usedIngredientCount": 2,
        "missedIngredientCount": 1
    }]

@pytest.fixture
def mock_scrape_data():
    return {
        'title': 'Test Recipe',
        'ingredients': ['1 cup sugar', '2 eggs'],
        'instructions': ['Mix ingredients', 'Bake at 350F']
    }

def test_home(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to your recipes discovery journey!" in response.data
    assert b"Find Recipes" in response.data

def test_get_recipes_success(test_client, mock_spoonacular_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_spoonacular_response
        
        form_data = {
            'ingredients': 'tomato,cheese',
            'submit': 'Submit'
        }
        response = test_client.post('/', 
                                  data=form_data, 
                                  follow_redirects=True)
        
        assert response.status_code == 200
        html_response = response.data.decode('utf-8')
        assert 'Recipe Suggestions' in html_response
        assert 'Test Recipe' in html_response
        assert 'See Recipe' in html_response

def test_get_recipes_api_failure(test_client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        
        form_data = {
            'ingredients': 'tomato,cheese',
            'submit': 'Submit'
        }
        response = test_client.post('/', 
                                  data=form_data, 
                                  follow_redirects=True)
        
        assert response.status_code == 200
        html_response = response.data.decode('utf-8')
        assert 'No recipes to display' in html_response

def test_recipe_route_success(test_client, mock_scrape_data):
    with patch('main.scrape_recipe') as mock_scrape:
        mock_scrape.return_value = mock_scrape_data
        
        response = test_client.post('/recipe', 
                                  data={'recipe_url': 'https://example.com/recipe'}, 
                                  follow_redirects=True)
        
        assert response.status_code == 200
        html_response = response.data.decode('utf-8')
        assert 'Test Recipe' in html_response
        assert 'Ingredients' in html_response
        assert 'Instructions' in html_response
        assert '1 cup sugar' in html_response
        assert 'Mix ingredients' in html_response

def test_recipe_route_failure(test_client):
    with patch('main.scrape_recipe') as mock_scrape:
        mock_scrape.return_value = None
        
        response = test_client.post('/recipe', 
                                  data={'recipe_url': 'https://example.com/bad-recipe'}, 
                                  follow_redirects=True)
        
        assert response.status_code == 200
        html_response = response.data.decode('utf-8')
        assert 'No recipes to display' in html_response
