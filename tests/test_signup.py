"""Tests for signup endpoint using AAA (Arrange-Act-Assert) pattern"""
import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_successful_signup_with_new_email(self, client, clean_activities):
        """Test successful signup when email is not already registered"""
        # Arrange: Prepare test data
        activity_name = "Art Club"
        email = "new.student@student.edu"
        
        # Act: Send signup request
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify signup was successful
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_adds_participant_to_activity(self, client, clean_activities):
        """Test that signup actually adds the email to activity participants"""
        # Arrange: Prepare test data
        activity_name = "Art Club"
        email = "new.student@student.edu"
        
        # Act: Sign up student and verify in activity list
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert: Verify participant was added
        assert email in activities[activity_name]["participants"]

    def test_duplicate_signup_returns_error(self, client, clean_activities):
        """Test that signing up with an already registered email returns error"""
        # Arrange: Use email already in Chess Club
        activity_name = "Chess Club"
        email = "existing@student.edu"
        
        # Act: Attempt to sign up with already-registered email
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify error response
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_to_activity_at_capacity_returns_error(self, client, clean_activities):
        """Test that signup fails when activity has reached max participants"""
        # Arrange: Full Activity has max_participants=1 and is full
        activity_name = "Full Activity"
        email = "trying.to.join@student.edu"
        
        # Act: Attempt to sign up for a full activity
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify error response
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        # The error might say "full" or "capacity" or "max_participants"

    def test_signup_to_nonexistent_activity_returns_404(self, client, clean_activities):
        """Test that signing up for a non-existent activity returns 404"""
        # Arrange: Use activity that doesn't exist
        activity_name = "Nonexistent Activity"
        email = "student@student.edu"
        
        # Act: Attempt to sign up for non-existent activity
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify 404 response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_without_email_parameter(self, client, clean_activities):
        """Test that signup without email parameter is handled"""
        # Arrange: Activity name without email parameter
        activity_name = "Art Club"
        
        # Act: Attempt signup without providing email
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert: Verify error response (email should be required)
        # Note: FastAPI might return 422 for missing required parameters
        assert response.status_code in [400, 422]

    def test_multiple_different_signups_to_same_activity(self, client, clean_activities):
        """Test that multiple different emails can sign up for the same activity"""
        # Arrange: Prepare activity with capacity for 2 participants
        activity_name = "Art Club"
        email1 = "student1@student.edu"
        email2 = "student2@student.edu"
        
        # Update Art Club capacity for this test
        from src.app import activities
        activities["Art Club"]["max_participants"] = 2
        
        # Act: Sign up two different students
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert: Both signups should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are in participants
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants

    def test_signup_response_contains_message(self, client, clean_activities):
        """Test that successful signup response contains a message"""
        # Arrange: Prepare test data
        activity_name = "Art Club"
        email = "success@student.edu"
        
        # Act: Send signup request
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify response structure
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0
