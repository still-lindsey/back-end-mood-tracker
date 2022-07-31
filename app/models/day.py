from tokenize import String

from sqlalchemy import null
from app import db
from sqlalchemy.sql import func
from .entry import Entry

class Day(db.Model):
	day_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	date = db.Column("date", db.String, nullable = False)
	day_of_week = db.Column("day_of_week", db.String, nullable = False)
	month = db.Column("month", db.String, nullable = False)
	quote = db.Column("quote", db.String)
	quote_author = db.Column("quote_author", db.String)
	# pictures = db.Column("photos", db.ARRAY(db.String))  THIS WOULD BE A SEPARATE MODEL
	# color = db.Column("color", db.String) THIS IS STRETCH GOAL, based on avg mood score from entry
	entries = db.relationship("Entry", back_populates = "day", lazy = True)
	
	def to_json(self):
		entries = [item.to_json() for item in self.entries]
		return {"date": self.date,
				"day_of_week": self.day_of_week,
				"month": self.month,
				"day_id": self.day_id,
				"quote": self.quote,
                "quote_author": self.quote_author,
				"entries": entries
			}
        
			
	@classmethod
	def create(cls, date, dayOfWeek, Month, req_body):
		new_entry = cls(
			quote = req_body[0]["q"],
			quote_author = req_body[0]["a"],
            date = date,
			day_of_week = dayOfWeek,
			month = Month)
			# pictures = req_body["pictures"]
		return new_entry	