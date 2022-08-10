from app import db



class Day(db.Model):
	day_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	month = db.relationship("Month", back_populates = "days")
	month_id = db.Column(db.Integer, db.ForeignKey('month.month_id'))
	date = db.Column("date", db.String, nullable = False)
	day_of_week = db.Column("day_of_week", db.String, nullable = False)
	month_name = db.Column("month_string", db.String, nullable = False)
	quote = db.Column("quote", db.String)
	quote_author = db.Column("quote_author", db.String)
	entries = db.relationship("Entry", back_populates = "day", lazy = True)
	# pictures = db.Column("photos", db.ARRAY(db.String))  THIS WOULD BE A SEPARATE MODEL
	# color = db.Column("color", db.String) THIS IS STRETCH GOAL, based on avg mood score from entry

	
	def to_json(self):
		entries = [item.to_json() for item in self.entries]
		return {"date": self.date,
				"day_of_week": self.day_of_week,
				"month": self.month_name,
				"day_id": self.day_id,
				"quote": self.quote,
                "quote_author": self.quote_author,
				"entries": entries,
				"month_id": self.month_id
			}
        
			
	@classmethod
	def create(cls, date, day_of_week, month, req_body):
		new_entry = cls(
			quote = req_body[0]["q"],
			quote_author = req_body[0]["a"],
            date = date,
			day_of_week = day_of_week,
			month_name = month)
			# pictures = req_body["pictures"]
		return new_entry	