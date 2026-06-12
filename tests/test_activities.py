"""Tests for activity endpoints using AAA (Arrange-Act-Assert) pattern"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_all_activities(self, client, clean_activities):
        """Test that GET /activities returns all activities"""
        # Arrange: No setup needed, activities already loaded in fixture
        
        # Act: Make request to get all activities
        response = client.get("/activities")
        
        # Assert: Verify response status and content
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert "Chess Club" in data
        assert "Art Club" in data
        assert "Full Activity" in data

    def test_activity_has_required_fields(self, client, clean_activities):
        """Test that each activity contains required fields"""
        # Arrange: Get activities
        response = client.get("/activities")
        data = response.json()
        
        # Act: Check Chess Club structure
        chess_club = data["Chess Club"]
        
        # Assert: Verify all required fields are present
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_activity_description_is_string(self, client, clean_activities):
        """Test that activity descriptions are strings"""
        # Arrange: Get activities
        response = client.get("/activities")
        data = response.json()
        
        # Act & Assert: Verify description field type for each activity
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0

    def test_activity_schedule_is_string(self, client, clean_activities):
        """Test that activity schedules are strings"""
        # Arrange: Get activities
        response = client.get("/activities")
        data = response.json()
        
        # Act & Assert: Verify schedule field type for each activity
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0

    def test_activity_max_participants_is_positive_integer(self, client, clean_activities):
        """Test that max_participants is a positive integer"""
        # Arrange: Get activities
        response = client.get("/activities")
        data = response.json()
        
        # Act & Assert: Verify max_participants for each activity
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0

    def test_participants_is_list_of_strings(self, client, clean_activities):
        """Test that participants list contains email strings"""
        # Arrange: Get activities
        response = client.get("/activities")
        data = response.json()
        
        # Act & Assert: Verify participants list structure
        for activity_name, activity_data in data.items():
            participants = activity_data["participants"]
            assert isinstance(participants, list)
            for participant in participants:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation

    def test_activity_with_existing_participants(self, client, clean_activities):
        """Test that activity correctly displays existing participants"""
        # Arrange: Get activities (Chess Club has one participant)
        response = client.get("/activities")
        data = response.json()
        
        # Act: Check Chess Club participants
        chess_club = data["Chess Club"]
        
        # Assert: Verify correct participants are shown
        assert len(chess_club["participants"]) == 1
        assert "existing@student.edu" in chess_club["participants"]

    def test_activity_with_no_participants(self, client, clean_activities):
        """Test that activity with no participants shows empty list"""
        # Arrange: Get activities (Art Club has no participants)
        response = client.get("/activities")
        data = response.json()
        
        # Act: Check Art Club participants
        art_club = data["Art Club"]
        
        # Assert: Verify participants list is empty
        assert len(art_club["participants"]) == 0
        assert isinstance(art_club["participants"], list)
