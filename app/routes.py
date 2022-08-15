from app import db
from datetime import datetime
from flask import Blueprint, jsonify, request, make_response, abort
import requests
from .models.day import Day
from .models.entry1 import Entry
from .models.month import Month
from .helpers import validate_record, is_new_day, get_daily_quote, get_month_id, get_top_3_frequent_activities, get_avg_mood_score_per_day_in_given_month,get_mood_by_activity, get_mood_by_feeling, get_top_3_frequent_feelings
import random
days_bp = Blueprint('days_bp', __name__, url_prefix="/days")

#user opened app
#view current day info 
@days_bp.route("", methods=["POST"])
def create_day():
	request_body = request.get_json()
	if request_body == None:
		LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo 
		#every time the app is opened make a call to post new month and day
		date = datetime.now(LOCAL_TIMEZONE)
		#reformat to 8 char string date since it will be easy to parse
		datestr = date.strftime("%Y") + date.strftime("%m") + date.strftime("%d")
		datestr_month = date.strftime("%m")
		datestr_year = date.strftime("%Y")
		day_of_week = date.strftime("%A")
		month = date.strftime("%B")
	else:
		datestr = request_body["date"]
		day_of_week = request_body["day_of_week"]
		month = request_body["month"]
		datestr_month = datestr[4:6]
		datestr_year = datestr[0:4]



	# #########building test cases for analytics page rendering
	# datestr = "20220731" #to change
	# datestr_month = "07" #to change
	# datestr_year = "2022" #to change
	# day_of_week = "Monday"
	# month = "July"
	# ########

	#get quote from external api
	response = get_daily_quote()

	month_id=get_month_id(datestr_month, datestr_year)
	if is_new_day(datestr):
		new_day = Day.create(datestr, day_of_week, month, response)

	db.session.add(new_day)
	month = Month.query.get(month_id)
	month.days.append(new_day)
	db.session.commit()

	result = new_day.to_json()
	result["status"] = "just created"

	return result, 201

#for testing my timeAgo functions in front end display all days
@days_bp.route("/<day_id>", methods=["PATCH"])
def patch_date(day_id):
	day = Day.query.get(day_id)
	validate_record(Day, day_id)
	request_body = request.get_json()
	day.date = request_body["date"]
	db.session.commit()
	days_response = day.to_json()
	days_response["status"] = "patched"
	return jsonify(days_response), 204

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

	return new_entry.to_json(), 201

entries_bp = Blueprint('entries_bp', __name__, url_prefix="/entries")

@entries_bp.route("/<entry_id>", methods=["DELETE"])
def delete_entry_for(entry_id):
	entry = validate_record(Entry, entry_id)

	db.session.delete(entry)
	db.session.commit()

	return jsonify({"details":f'Entry {entry.entry_id} successfully deleted'}), 200

@days_bp.route("", methods=["DELETE"])
def delete_all_data():
	try: 
		db.session.query(Entry).delete()
		db.session.query(Day).delete()
		db.session.query(Month).delete()
		db.session.commit()
	except:
		db.session.rollback()
    
	return "Successfully deleted all data", 200

#get day by ID
#will come in handly if I can scroll and select days on the welcome page
@days_bp.route("/<day_id>", methods=["GET"])
def get_day_by(day_id):
	day = Day.query.get(day_id)
	validate_record(Day, day_id)

	days_response = day.to_json()
	days_response["status"] = "already created"
	return jsonify(days_response), 200

#get all days
#for view all days page
@days_bp.route("", methods=["GET"])
def get_all_days():
	days = Day.query.all()
	days_response = {}
	days_response = [day.to_json() for day in days]
	return jsonify(days_response), 200

quotes_bp = Blueprint('quotes_bp', __name__, url_prefix="/quotes")

#get random quote
#for random quote page
@quotes_bp.route("", methods=["GET"])
def get_random_quote():
	url = "https://zenquotes.io/api/random"

	response = requests.get(url)

	return response.json()[0], 200

#additional functionality to like and save quotes



#get previous month's analytics
months_bp = Blueprint('months_bp', __name__, url_prefix="/months")

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

#working!
#for monthly analytics page
@months_bp.route("/<month_id>/analytics", methods=["GET"])
def get_month_analytics(month_id):
	validate_record(Month, month_id)
	month = Month.query.get(month_id)
	#get list of month objects with non empty entries
	list_of_days_with_entries = []
	for day in month.days:
		if len(day.entries) > 0:
			list_of_days_with_entries.append(day) #day objects
	
	#handle empty month

	# if len(list_of_days_with_entries) == 0:
		# return abort(make_response({"message": f"Month {month_id} has no data. Please submit entries to see a report."}, 404))

	#make dictionary of day: average mood
	avg_mood_score_per_day_in_given_month = get_avg_mood_score_per_day_in_given_month(list_of_days_with_entries, month)
	
	#get average mood for whole month
	if len(list_of_days_with_entries) != 0: 
		average_mood_for_month = sum([value for value in avg_mood_score_per_day_in_given_month if value >= 0]) / len([value for value in avg_mood_score_per_day_in_given_month if value >= 0])
	else:
		average_mood_for_month = 0.0
	#get positive days objects
	positive_days = [day for day in list_of_days_with_entries if avg_mood_score_per_day_in_given_month[int(day.date[6:8]) - 1] >= 5.0]
	#get positive days objects
	negative_days = [day for day in list_of_days_with_entries if avg_mood_score_per_day_in_given_month[int(day.date[6:8]) - 1] < 5.0 and avg_mood_score_per_day_in_given_month[int(day.date[6:8]) - 1] >= 0]
	#get num pos days
	num_positive_days = len(positive_days)
	#get num neg days
	num_negative_days = len(negative_days)


	mood_by_activity, entry_count = get_mood_by_activity(list_of_days_with_entries)
	mood_by_feeling = get_mood_by_feeling(list_of_days_with_entries)

	positive_activities = [key for key, value in mood_by_activity.items() if (value["aggregated_mood_score"] / value["freq"]) >= 5.0]
	negative_activities = [key for key, value in mood_by_activity.items() if (value["aggregated_mood_score"] / value["freq"]) < 5.0]
	
	top_3_frequent_activities = get_top_3_frequent_activities(mood_by_activity, entry_count)

	top_3_frequent_feelings = get_top_3_frequent_feelings(mood_by_feeling, entry_count)

	response = {"month_average_mood": average_mood_for_month, 
	"days_average_moods": avg_mood_score_per_day_in_given_month,
	"num_positive_days": num_positive_days,
	"num_negative_days": num_negative_days,
	"positive_activities": positive_activities,
	"negative_activities": negative_activities,
	"mood_by_activity": mood_by_activity,
	"top_three_activities_freq": top_3_frequent_activities,
	"top_three_feelings_freq": top_3_frequent_feelings}
	return jsonify(response), 200
 


#Days to Post


post = {
"title": "Cooking",
"memo": "Cooked a tofu hamburger steak and it was amazing...crispy on the outside and juicy on the inside...I've truly outdone myself.",
"mood_score": 4.0,
"activities": ["hobbies", "friends"],
"emotions": ["happy", "loved", "excited", "confused"],
"time_stamp": "Wed, 10 Aug 2022 10:43:20 GMT"
}

@months_bp.route("", methods=["POST"])
def post_test_days():
	for i in range(27,57):
		post["mood_score"] = random.uniform(0.0, 10.0)
		if post["mood_score"]  > 5.0:
			post["activities"] = ["hobbies", "friends", "art"]
			post["emotions"] = ["happy", "loved", "excited"]
		else: 
			post["activities"] = ["work", "sleep", "weather"]
			post["emotions"] = ["sad", "confused", "worried"]

		try:
			new_entry = Entry.create(post, i)
		except KeyError:
			return abort(make_response(jsonify({"details":"Invalid data"}), 400))

		db.session.add(new_entry)
		db.session.commit()

	return new_entry.to_json(), 201