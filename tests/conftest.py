import pytest
from app import db
from app import create_app
from app.models.day import Day
from app.models.entry1 import Entry
from app.models.month import Month


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture creates a single card and saves it in the database
# References "one_card"
@pytest.fixture
def one_month(app):
    new_month = Month(
        this_year="2022",
        this_month = "07")
    db.session.add(new_month)
    db.session.commit()

@pytest.fixture
def one_day(app):
    new_day = Day(
        quote="Get some sunshine, its good for you!☀️ 😎 ",
        author = "Lindsey",
        date = "20220701",
        day_of_week = "Monday",
        month_name = "July")
    db.session.add(new_day)
    month = Month.query.get(1)
    month.days.append(new_day)
    db.session.commit()


# This fixture creates a single board and saves it in the database
# References "one_board"
@pytest.fixture
def one_entry(app):
    new_entry = Entry(
        	title = "Hi",
			memo = "A great dayyyy",
			mood_score = 7,
			activities = ["food", "hobbies"],
			emotions = ["relaxed"],
			day_id = 1)
    db.session.add(new_entry)
    db.session.commit()

# This fixture creates a single board and a single card and saves it in the database
# References "one_card_belongs_to_one_goal"
@pytest.fixture
def one_entry_belongs_to_one_day(app, one_day, one_entry):
    entry = Entry.query.first()
    day = Day.query.first()
    day.entries.append(entry)
    db.session.commit()
