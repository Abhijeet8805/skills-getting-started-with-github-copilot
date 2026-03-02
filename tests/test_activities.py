"""Tests for the activities endpoint"""


class TestGetActivities:
    """Test the GET /activities endpoint"""

    def test_returns_all_activities(self, client, reset_activities):
        """ARRANGE: Activities are initialized
           ACT: client requests all activities
           ASSERT: returns all activities with correct structure
        """
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(activities_data) == 3  # Chess Club, Programming Class, Art Studio
        assert "Chess Club" in activities_data
        
        # Verify structure
        for activity_name, activity_info in activities_data.items():
            assert set(activity_info.keys()) == expected_keys

    def test_activities_have_participants_count(self, client, reset_activities):
        """ARRANGE: Activities with participants are initialized
           ACT: client requests activities
           ASSERT: participant lists are accessible
        """
        # Arrange
        # (already set up in fixture)
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        chess_club = activities_data["Chess Club"]
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]

    def test_activities_include_max_participants(self, client, reset_activities):
        """ARRANGE: Activities with max_participants set
           ACT: client requests activities
           ASSERT: max_participants is returned
        """
        # Arrange
        # (already set up in fixture)
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        programming = activities_data["Programming Class"]
        assert programming["max_participants"] == 20
