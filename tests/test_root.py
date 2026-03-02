"""Tests for root endpoint redirect"""


class TestRootEndpoint:
    """Test the GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        """ARRANGE: Request root endpoint
           ACT: client makes GET request
           ASSERT: should redirect to /static/index.html
        """
        # Arrange
        expected_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_url
