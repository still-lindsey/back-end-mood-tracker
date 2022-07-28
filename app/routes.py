from datetime import datetime
from flask import Blueprint, jsonify, request, make_response, abort, json
from app import db
from app.models.day import Day
from app.models.entry import Entry
from app import db
from .helpers import validate_record, is_new_day, get_daily_quote

days_bp = Blueprint('days_bp', __name__, url_prefix="/days")

#user opened app 
@days_bp.route("", methods=["POST"])
def create_day():
	#every time the app is opened make a call to post new day
	date = datetime.now()
	#reformat to 8 char string date since it will be easy to parse
	datestr = date.strftime("%Y") + date.strftime("%m") + date.strftime("%d")
	#get quote from external api
	response = get_daily_quote()
	try:
		if is_new_day(datestr):
			new_day = Day.create(datestr, response)
	except KeyError:
		return abort(make_response(jsonify({"details":"Invalid data"}), 400))

	db.session.add(new_day)
	db.session.commit()

	return {new_day.date: new_day.to_json()}, 201

#post new entry
@days_bp.route("/<day_id>/entries", methods=["POST"])
def create_entry_for(day_id):
	validate_record(Day, day_id)
	request_body = request.get_json()
	try:
		new_entry = Entry.create(request_body, day_id)
	except KeyError:
		return abort(make_response(jsonify({"details":"Invalid data"}), 400))

	db.session.add(new_entry)
	db.session.commit()

	return {"entry": new_entry.to_json()}, 201

#get day by ID
@days_bp.route("/<day_id>", methods=["GET"])
def get_day_by(day_id):
	day = Day.query.get(day_id)
	validate_record(Day, day_id)

	days_response = day.to_json()
	return jsonify(days_response), 200

#get all days
@days_bp.route("", methods=["GET"])
def get_all_days():
	days = Day.query.all()
	days_response = {}
	days_response = {day.date: day.to_json() for day in days}
	return jsonify(days_response), 200

quotes_bp = Blueprint('quotes_bp', __name__, url_prefix="/quotes")

@quotes_bp.route("", methods=["GET"])
def get_random_quote():
	url = "https://zenquotes.io/api/random"

	response = request.get(url)

	return response.json()

#additional functionality to like and save quotes



#get previous month's analytics
analytics_bp = Blueprint('analytics_bp', __name__, url_prefix="/analytics")

DAYS_IN_EACH_MONTH = {
	"01": 31,
	"02": 28,
	"03": 31,
	"04": 30,
	"05": 31,
	"06": 30,
	"07": 31,
	"08": 31,
	"09": 30,
	"10": 31,
	"11": 30,
	"12": 31
}

@analytics_bp.route("/<day_id>", methods=["GET"])
def get_month_analytics(day_id):
	#logic to identify previous month
		date = Day.query.get(day_id)
		date = date.to_json()
		year = date.date[0:4]
		month = date.date[4:6]
	
	#get list of month objects with non empty entries
		list_of_days_with_entries = []

		for i in range(DAYS_IN_EACH_MONTH[month]):
			if i < 10:
				date = year + month + "0" + str(i)
				date_object = Day.query.filter_by(date=date).first()
				if date_object and date_object.to_json().entries:
					list_of_days_with_entries.append(date_object.to_json())
			if i >= 10:
				date = year + month + str(i)
				date_object = Day.query.filter_by(date=date).first()
				if date_object and date_object.to_json().entries:
					list_of_days_with_entries.append(date_object.to_json())

	#make dictionary of day: average mood


	#return day > average mood for that day plus average mood overall 

