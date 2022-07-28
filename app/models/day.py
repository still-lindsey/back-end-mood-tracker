from tokenize import String

from sqlalchemy import null
from app import db
from sqlalchemy.sql import func
from .entry import Entry

class Day(db.Model):
	day_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	date = db.Column("date", db.String, nullable = False)
	quote = db.Column("quote", db.String)
	quote_author = db.Column("quote_author", db.String)
	# pictures = db.Column("photos", db.ARRAY(db.String))  THIS WOULD BE A SEPARATE MODEL
	entries = db.relationship("Entry", back_populates = "day", lazy = True)
	
	def to_json(self):
		entries = [item.to_json() for item in self.entries]
		return {"day_id": self.day_id,
				"quote": self.quote,
                "quote_author": self.quote_author,
				"entries": entries,
                "date": self.date
			}
        
			
	@classmethod
	def create(cls, date, req_body):
		new_entry = cls(
			quote = req_body[0]["q"],
			quote_author = req_body[0]["a"],
            date = date
			# pictures = req_body["pictures"]
		)
		return new_entry	