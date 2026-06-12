import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for making API requests"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to a known test state before each test"""
    # Store original activities
    original_activities = {
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()
        }
        for key, value in activities.items()
    }
    
    yield
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def clean_activities(reset_activities):
    """Provide a fresh set of activities with minimal test data"""
    # Clear all participants and keep only essential activities
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["existing@student.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 1,
            "participants": []
        },
        "Full Activity": {
            "description": "An activity at capacity",
            "schedule": "Mondays, 4:00 PM - 5:00 PM",
            "max_participants": 1,
            "participants": ["full@student.edu"]
        }
    })
