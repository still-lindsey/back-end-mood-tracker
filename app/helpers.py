from flask import Blueprint, jsonify, request, make_response, abort
from .models.month import Month
from .models.day import Day
from app import db
import requests
from datetime import datetime

def validate_record(cls, id):
	try:
		id = int(id)
	except ValueError:
		abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

	obj = cls.query.get(id)

	if not obj:
		return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

	return obj

def get_month_id(new_month, new_year):
	months = Month.query.all()

	for month in months:
		if month.this_month == new_month and month.this_year == new_year:
			month_id = month.month_id
			return month_id
	
	new_month = Month.create(new_month, new_year)
	month_id = new_month.month_id
	db.session.add(new_month)
	db.session.commit()
	return month_id
	

def is_new_day(date):
	days = Day.query.all()

	for day in days:
		if day.date == date:
			result = day.to_json()
			result["status"] = "already created"
			#Instead of makeing a response with code 201, I should call the get method. BUT my front end requires
			#201 message to work
			return abort(make_response(result, 201))
	
	return True

def get_daily_quote():
	url = "https://zenquotes.io/api/today"

	response = requests.get(url)

	return response.json()

def get_top_3_frequent_activities(mood_by_activities, entry_count):
	top_3_most_freq_activities = []
	if entry_count == 0:
		return top_3_most_freq_activities
	mood_by_activities_copy = mood_by_activities.copy()
	count = 3
	while count > 0:
		max_freq = 0
		max_activity = None
		for activity, value in mood_by_activities_copy.items():
			if value["freq"] > max_freq: #does not account for ties
				max_freq = value["freq"]
				max_activity = activity
		top_3_most_freq_activities.append({"activity": max_activity, "frequency": max_freq / entry_count})
		del mood_by_activities_copy[max_activity]
		count -= 1
	return top_3_most_freq_activities

def get_top_3_frequent_feelings(mood_by_feelings, entry_count):

	top_3_most_freq_feelings = []
	if entry_count == 0:
		return top_3_most_freq_feelings
	mood_by_feelings_copy = mood_by_feelings.copy()
	count = 3
	while count > 0:
		max_freq = 0
		max_feeling = None
		for feeling, value in mood_by_feelings_copy.items():
			if value["freq"] > max_freq: #does not account for ties
				max_freq = value["freq"]
				max_feeling = feeling
		top_3_most_freq_feelings.append({"feeling": max_feeling, "frequency": max_freq / entry_count})
		del mood_by_feelings_copy[max_feeling]
		count -= 1
	return top_3_most_freq_feelings

def get_avg_mood_score_per_day_in_given_month(list_of_days_with_entries, month):
	avg_mood_score_per_day_in_given_month = [-0.1] * 31
	if len(list_of_days_with_entries) == 0:
		return avg_mood_score_per_day_in_given_month
	index = 0
	for i in range(len(avg_mood_score_per_day_in_given_month)):
		if index < len(list_of_days_with_entries):
			day_of_month = list_of_days_with_entries[index].date[6:8] 
		if index < len(list_of_days_with_entries) and int(day_of_month) == (i + 1):
			avg_mood_per_day = 0
			for entry in list_of_days_with_entries[index].entries:
				avg_mood_per_day += entry.mood_score
			avg_mood_per_day = avg_mood_per_day / len(list_of_days_with_entries[index].entries)
			avg_mood_score_per_day_in_given_month[i] = avg_mood_per_day
			index += 1
		else:
			continue
	return avg_mood_score_per_day_in_given_month

def get_mood_by_activity(list_of_days_with_entries):
	mood_by_activities = {} #shape= {"exercise": {"freq": 3, "aggregated_mood_score": 24.6}, "work": {"freq": 5, "aggregated_mood_score": 36.0}}
	entry_count = 0
	for day in list_of_days_with_entries:
		for entry in day.entries:
			entry_count += 1
			for activity in entry.activities:
				if mood_by_activities.get(activity) != None:
					mood_by_activities[activity]["freq"] += 1
					mood_by_activities[activity]["aggregated_mood_score"] += entry.mood_score
				else:
					mood_by_activities[activity] = {"freq": 1, "aggregated_mood_score": entry.mood_score}

	return mood_by_activities, entry_count

def get_mood_by_feeling(list_of_days_with_entries):
	mood_by_feeling = {} #shape= {"sad": {"freq": 3, "aggregated_mood_score": 24.6}, "annoyed": {"freq": 5, "aggregated_mood_score": 36.0}}
	for day in list_of_days_with_entries:
		for entry in day.entries:
			for feeling in entry.emotions:
				if mood_by_feeling.get(feeling) != None:
					mood_by_feeling[feeling]["freq"] += 1
					mood_by_feeling[feeling]["aggregated_mood_score"] += entry.mood_score
				else:
					mood_by_feeling[feeling] = {"freq": 1, "aggregated_mood_score": entry.mood_score}

	return mood_by_feeling