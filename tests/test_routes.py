from app.models.day import Day
import pytest

# Test GET Boards returns empty list
# @pytest.mark.skip
def test_get_entries_no_saved_days(client):
    # Act
    response = client.get("/days")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# Test GET one Board returns Board
# @pytest.mark.skip
def test_get_days_one_saved_day(client):
    # Act
    response = client.get("/days")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "title": "Hi",
			"memo":"A great dayyyy",
			"mood_score": 7,
			"activities": ["food", "hobbies"],
			"emotions": ["relaxed"],
			"day_id": 1
        }
    ]

# Test POST one board returns Board
# @pytest.mark.skip
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Another very inspirational board",
        "owner": "Lindsey",
        "color": "39166F"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Another very inspirational board",
            "owner": "Lindsey",
            "cards": [],
            "color": "39166F"
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "Another very inspirational board"
    assert new_board.owner == "Lindsey"
    assert new_board.cards == []

# Test GET Cards from Board
# @pytest.mark.skip
def test_get_cards_for_specific_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 1
    assert response_body == {
        "board_id": 1,
        "title": "camelCase Inspiration",
        "owner": "Poppy",
        "cards": [
            {
                "card_id": 1,
                "message": "Get some sunshine, its good for you!☀️ 😎 ",
                "likes_count": 0,
                "board_id": 1
            }
        ],
        "color": "39166F"
    }

# Test POST Cards from Board
# @pytest.mark.skip
def test_post_card_to_board(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Hi, this is a test card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board_id" in response_body
    assert "card_id" in response_body
    assert "likes_count" in response_body
    assert "message" in response_body
    assert response_body == {
        "board_id": 1,
        "card_id": 1,
        "likes_count": 0,
        "message": "Hi, this is a test card"
    }

    # Check that Board was updated in the db
    assert len(Day.query.get(1).cards) == 1