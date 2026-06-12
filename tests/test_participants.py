"""Tests for participant removal endpoint using AAA (Arrange-Act-Assert) pattern"""
import pytest


class TestRemoveParticipant:
    """Test suite for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_successful_participant_removal(self, client, clean_activities):
        """Test successful removal of an existing participant"""
        # Arrange: Use existing participant in Chess Club
        activity_name = "Chess Club"
        email = "existing@student.edu"
        
        # Act: Send delete request
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert: Verify deletion was successful
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_participant_removed_from_activity_list(self, client, clean_activities):
        """Test that participant is actually removed from the activity"""
        # Arrange: Use existing participant in Chess Club
        activity_name = "Chess Club"
        email = "existing@student.edu"
        
        # Verify participant exists before deletion
        response_before = client.get("/activities")
        participants_before = response_before.json()[activity_name]["participants"]
        assert email in participants_before
        
        # Act: Delete the participant
        client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert: Verify participant is no longer in list
        response_after = client.get("/activities")
        participants_after = response_after.json()[activity_name]["participants"]
        assert email not in participants_after

    def test_remove_nonexistent_participant_returns_404(self, client, clean_activities):
        """Test that removing a non-existent participant returns 404"""
        # Arrange: Use email not in Art Club
        activity_name = "Art Club"
        email = "nonexistent@student.edu"
        
        # Act: Attempt to remove non-existent participant
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert: Verify 404 response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_returns_404(self, client, clean_activities):
        """Test that removing from non-existent activity returns 404"""
        # Arrange: Use activity that doesn't exist
        activity_name = "Nonexistent Activity"
        email = "student@student.edu"
        
        # Act: Attempt to remove from non-existent activity
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert: Verify 404 response
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_participant_count_decreases_after_removal(self, client, clean_activities):
        """Test that participant count decreases after removing a participant"""
        # Arrange: Get initial count for Chess Club
        response_before = client.get("/activities")
        count_before = len(response_before.json()["Chess Club"]["participants"])
        
        # Act: Remove the existing participant
        client.delete(
            f"/activities/Chess Club/participants/existing@student.edu"
        )
        
        # Assert: Verify count decreased by 1
        response_after = client.get("/activities")
        count_after = len(response_after.json()["Chess Club"]["participants"])
        assert count_after == count_before - 1

    def test_remove_participant_allows_new_signup(self, client, clean_activities):
        """Test that removing a participant frees up a spot for new signups"""
        # Arrange: Chess Club is at capacity (2 max, 1 existing)
        activity_name = "Chess Club"
        existing_email = "existing@student.edu"
        new_email1 = "new1@student.edu"
        new_email2 = "new2@student.edu"
        
        # Verify we can add one more participant
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email1}
        )
        assert response1.status_code == 200
        
        # Verify activity is now at capacity
        response_before = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email2}
        )
        assert response_before.status_code == 400
        
        # Act: Remove the existing participant to free a spot
        client.delete(
            f"/activities/{activity_name}/participants/{existing_email}"
        )
        
        # Assert: Now new_email2 should be able to sign up
        response_after = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email2}
        )
        assert response_after.status_code == 200

    def test_remove_response_contains_message(self, client, clean_activities):
        """Test that remove response contains a message"""
        # Arrange: Prepare test data
        activity_name = "Chess Club"
        email = "existing@student.edu"
        
        # Act: Send delete request
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert: Verify response structure
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0

    def test_remove_same_participant_twice_fails(self, client, clean_activities):
        """Test that removing the same participant twice returns error on second attempt"""
        # Arrange: Prepare test data
        activity_name = "Chess Club"
        email = "existing@student.edu"
        
        # Act: Remove participant first time
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert: First removal succeeds
        assert response1.status_code == 200
        
        # Act: Attempt to remove same participant again
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert: Second removal fails with 404
        assert response2.status_code == 404
