from tokenize import String

from sqlalchemy import null
from app import db
from sqlalchemy.sql import func
from .entry import Entry

class Month(db.Model):
	month_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	this_year = db.Column("this_year", db.String, nullable = False) 
	this_month = db.Column("this_month", db.String, nullable = False)
	days = db.relationship("Day", back_populates = "month", lazy = True)
	
	def to_json(self):
		days = [item.to_json() for item in self.days]
		return {"month_id": self.month_id,
                "year": self.this_year,
                "month": self.this_month,
				"days": days
			}
        
			
	@classmethod
	def create(cls, this_month, this_year):
		new_month = cls(
			this_year = this_year,
            this_month = this_month)
			# pictures = req_body["pictures"]
		return new_month	