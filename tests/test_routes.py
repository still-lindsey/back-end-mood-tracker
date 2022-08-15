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
def test_get_days_one_saved_day(client, one_month, one_day):
    # Act
    response = client.get("/days")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["date"] == "20220701"

# # Test POST one board returns Board
# @pytest.mark.skip
def test_create_day(client, three_months):
    # Act
    response = client.post("/days", json={
        "date": "20220601",
        "day_of_week": "Monday",
        "month": "July"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert len(response_body["date"]) == 8


def test_add_entry(client, three_months, one_day):
    # Act
    response = client.post("/days/1/entries", json={
"title": "Cooking",
"memo": "Cooked a tofu hamburger steak and it was amazing...crispy on the outside and juicy on the inside...I've truly outdone myself.",
"mood_score": 7,
"activities": ["hobbies", "friends"],
"emotions": ["happy", "loved"],
"time_stamp": "Wed, 10 Aug 2022 10:43:20 GMT"
})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == "Cooking"

def test_add_entry_to_month_2(client, three_months_with_days_and_entries):
    response = client.post("/days/2/entries", json={
"title": "Cooking",
"memo": "Cooked a tofu hamburger steak and it was amazing...crispy on the outside and juicy on the inside...I've truly outdone myself.",
"mood_score": 7,
"activities": ["hobbies", "friends"],
"emotions": ["happy", "loved"],
"time_stamp": "Wed, 10 Aug 2022 10:43:20 GMT"
})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == "Cooking"

def test_number_of_entries_in_db_30(client, three_months_with_days_and_entries):
    response = client.get("/days")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 45
    assert len(response_body[0]["entries"]) == 1
    for day in response_body:
        assert len(day["entries"]) == 1

# # Test GET Cards from Board
# # @pytest.mark.skip
# def test_specific_day_entries(client, one_card_belongs_to_one_board):
#     # Act
#     response = client.get("/days/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert "cards" in response_body
#     assert len(response_body["cards"]) == 1
#     assert response_body == {
#         "board_id": 1,
#         "title": "camelCase Inspiration",
#         "owner": "Poppy",
#         "cards": [
#             {
#                 "card_id": 1,
#                 "message": "Get some sunshine, its good for you!☀️ 😎 ",
#                 "likes_count": 0,
#                 "board_id": 1
#             }
#         ],
#         "color": "39166F"
#     }

# # Test POST Cards from Board
# # @pytest.mark.skip
# def test_post_entry_to_one_Day(client, one_board):
#     # Act
#     response = client.post("/boards/1/cards", json={
#         "message": "Hi, this is a test card"
#     })
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert "board_id" in response_body
#     assert "card_id" in response_body
#     assert "likes_count" in response_body
#     assert "message" in response_body
#     assert response_body == {
#         "board_id": 1,
#         "card_id": 1,
#         "likes_count": 0,
#         "message": "Hi, this is a test card"
#     }

#     # Check that Board was updated in the db
#     assert len(Day.query.get(1).cards) == 1