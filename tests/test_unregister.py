"""Tests for unregister endpoint"""


class TestUnregisterFromActivity:
    """Test the DELETE /activities/{activity_name}/unregister endpoint"""

    def test_successful_unregister(self, client, reset_activities):
        """ARRANGE: Student currently signed up for activity
           ACT: DELETE request to unregister endpoint
           ASSERT: student is removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"
        
        # Verify student is signed up
        activities = client.get("/activities").json()
        assert student_email in activities[activity_name]["participants"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {student_email} from {activity_name}"
        
        # Verify student is removed
        activities = client.get("/activities").json()
        assert student_email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """ARRANGE: Invalid activity name
           ACT: DELETE request to nonexistent activity
           ASSERT: returns 404 error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_student_not_signed_up_returns_400(self, client, reset_activities):
        """ARRANGE: Student not signed up for activity
           ACT: DELETE request to unregister
           ASSERT: returns 400 error
        """
        # Arrange
        activity_name = "Programming Class"
        student_email = "notstudent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_unregister_decrements_participant_count(self, client, reset_activities):
        """ARRANGE: Activity with known participant count
           ACT: Existing student unregisters
           ASSERT: participant count decreases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "daniel@mergington.edu"
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        assert updated_count == initial_count - 1

    def test_cannot_unregister_twice(self, client, reset_activities):
        """ARRANGE: Student is unregistered
           ACT: Try to unregister the same student again
           ASSERT: returns 400 error on second attempt
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"
        
        # First unregister (should succeed)
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Act - Try to unregister again
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"
