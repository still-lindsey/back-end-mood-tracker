from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.entry import Entry
from app.models.day import Day
from app import db
import requests

def validate_record(cls, id):
	try:
		id = int(id)
	except ValueError:
		abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

	obj = cls.query.get(id)

	if not obj:
		return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

	return obj

def is_new_day(date):
	days = Day.query.all()

	for day in days:
		if day.date == date:
			return abort(make_response({"message": f"User already visited app on {date} and day has already been already created."}))
	
	return True

def get_daily_quote():
	url = "https://zenquotes.io/api/today"

	response = requests.get(url)

	return response.json()
