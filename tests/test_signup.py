"""Tests for signup endpoint"""


class TestSignupForActivity:
    """Test the POST /activities/{activity_name}/signup endpoint"""

    def test_successful_signup(self, client, reset_activities):
        """ARRANGE: New student email and existing activity
           ACT: POST request to signup endpoint
           ASSERT: student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"
        
        # Verify student is in participants list
        activities = client.get("/activities").json()
        assert student_email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """ARRANGE: Invalid activity name
           ACT: POST request to nonexistent activity
           ASSERT: returns 404 error
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        student_email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_duplicate_signup_returns_400(self, client, reset_activities):
        """ARRANGE: Student already signed up for activity
           ACT: Attempt to signup same student again
           ASSERT: returns 400 error (prevents double registration)
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_increments_participant_count(self, client, reset_activities):
        """ARRANGE: Activity with known participant count
           ACT: New student signs up
           ASSERT: participant count increases by 1
        """
        # Arrange
        activity_name = "Programming Class"
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])
        student_email = "newstudent@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        assert updated_count == initial_count + 1

    def test_signup_with_special_characters_in_email(self, client, reset_activities):
        """ARRANGE: Email with special characters (URL encoded)
           ACT: POST request with encoded email
           ASSERT: signup succeeds
        """
        # Arrange
        activity_name = "Art Studio"
        student_email = "student+art@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert student_email in activities[activity_name]["participants"]
