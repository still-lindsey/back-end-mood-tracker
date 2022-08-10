from app import db
from sqlalchemy.sql import func
from datetime import datetime


class Entry(db.Model):
	entry_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	day_id = db.Column(db.Integer, db.ForeignKey('day.day_id'))
	title = db.Column("title", db.String, nullable = False)
	memo = db.Column("memo", db.VARCHAR(1000), nullable = False)
	mood_score = db.Column("mood_score", db.Float, nullable = False)
	activities = db.Column("activities", db.ARRAY(db.String), nullable = False)
	emotions = db.Column("emotions", db.ARRAY(db.String), nullable = False)
	time_stamp = db.Column("time", db.DateTime, nullable = False)
	day = db.relationship("Day", back_populates = "entries")
	
	def to_json(self):
		return {"entry_id": self.entry_id,
				"title": self.title,
				"memo": self.memo,
				"mood_score": self.mood_score,
				"activities": self.activities,
				"emotions": self.emotions,
				"time_stamp": self.time_stamp
			}
			
	@classmethod
	def create(cls, req_body, day_id):
		new_entry = cls(
			title = req_body["title"],
			memo = req_body["memo"],
			mood_score = req_body["mood_score"],
			activities = req_body["activities"],
			emotions = req_body["emotions"],
			day_id = day_id,
			time_stamp = req_body["time_stamp"]
		)
		return new_entry	