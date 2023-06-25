from __future__ import print_function

import requests

from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Define your TMDB API key
api_key = "YOUR_TMDB_API_KEY"
# Define your Google Calendar ID
calendarId = 'YOUR_GOOGLE_CALENDAR_ID'

# Define the company IDs
companies_id = ["YOUR_COMPANIES_ID_HERE","YOUR_COMPANIES_ID2_HERE"]

# Define the region ("US","FR",...) for which you want to retrieve release dates and the output language ("us-US" for United-States, "fr-FR" for France...)
first_region = "US"
second_region = "FR"
language = "us-US"


def main():
    # Iterate through the movie results for each company ID
    for id in companies_id:
        data_movies = requete_tmdb_movie(api_key, id, "US")
        for movie in data_movies["results"]:
            title = movie["title"]
            release_date = movie["release_date"]
            poster = movie["poster_path"]
            synopsis = movie["overview"]
            release_date = requete_tmdb_movie_date(api_key, movie['id'], first_region)
            if release_date != "none":
                fr_release_date = release_date
                print(f"\n{title} {movie['id']} {fr_release_date} in {first_region}")
                providers = requete_tmdb_watch_providers(api_key, movie['id'], "movie", first_region)
                add_event(title, fr_release_date, creds, "movie", movie['id'], first_region, synopsis, providers=providers_string(providers))
            elif release_date == "none":
                us_release_date = requete_tmdb_movie_date(api_key, movie['id'], second_region)
                print(f"\n{title} {movie['id']} {us_release_date} in {second_region}")
                providers = requete_tmdb_watch_providers(api_key, movie['id'], "movie", first_region)
                add_event(title, us_release_date, creds, "movie", movie['id'], second_region, synopsis, providers=providers_string(providers))
            else:
                print(f"No release dates in {first_region} or {second_region}")

    # Iterate through the series results for each company ID
    for id in companies_id:
        data_series = requete_tmdb_serie(api_key, id, "US")
        if data_series["total_results"] >= 1:
            for serie in data_series["results"]:
                title = serie["name"]
                first_air_date = serie["first_air_date"]
                poster = serie["poster_path"]
                synopsis = serie["overview"]
                if first_air_date:
                    print(f"\n{title} {serie['id']} {first_air_date}")
                    providers = requete_tmdb_watch_providers(api_key, movie['id'], "TV", {first_region})
                    add_event(title, first_air_date, creds, "tv", serie['id'], "", synopsis, providers=providers_string(providers))
        else:
            print("No planned series")

# Function to refresh the access token if it's expired
def refresh_token(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        return True
    return False

# Function to get the user credentials
def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("No file named 'token.json'")
    return creds

# Function to save the user credentials
def save_credentials(creds):
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Load credentials
creds = get_credentials()

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if refresh_token(creds):
        save_credentials(creds)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        save_credentials(creds)

def requete_tmdb_movie(api_key, company_id, region):
    url_movies = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_companies={company_id}&region={region}&sort_by=release_date.asc&primary_release_date.gte=now&language={language}"
    #url_movies = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_companies={company_id}&region={region}&sort_by=release_date.asc&primary_release_year=2023&language=fr-FR"

    response_movies = requests.get(url_movies)
    data_movies = response_movies.json()
    return data_movies

def requete_tmdb_serie(api_key, company_id, region):
    url_series = f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&with_companies={company_id}&region={region}&sort_by=first_air_date.asc&first_air_date.gte=now&language={language}"
    #url_series = f"https://api.themoviedb.org/3/discover/tv?api_key={api_key}&with_companies={company_id}&region={region}&sort_by=first_air_date.asc&first_air_date_year=2023&language=fr-FR"

    response_series = requests.get(url_series)
    data_series = response_series.json()
    return data_series

def requete_tmdb_movie_date(api_key, movie_id, region):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    spc_release_date = "none"
    for release in data["results"]:
        if release["iso_3166_1"] == region:
            for release_date in release["release_dates"]:
                spc_release_date = release_date["release_date"].split("T")[0]
            break
    return spc_release_date

def requete_tmdb_watch_providers(api_key, movie_id, type, region):
    url = f"https://api.themoviedb.org/3/{type}/{movie_id}/watch/providers?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    fr_providers = {}
    for i in ["flatrate", "buy", "free"]:
        try:
            fr_providers[i] = ([provider['provider_name'] for provider in data['results'][region][i]])
        except:
            continue
    return fr_providers

def providers_string(providers):
    if providers:
        provider_txt = 'Watch on: '

        for i in ["flatrate", "buy", "free"]:
            try:
                provider_txt += ', '.join(providers[i])
                provider_txt += f' ({i}) '
            except:
                continue
    else:
        provider_txt = ""
    return provider_txt

def add_event(title, release_date, creds, type_show, ID, region, synopsis, providers):

    
    service = build('calendar', 'v3', credentials=creds)
    if type_show == 'tv':
        title_and_type = f"{title} (TV Series)"
    else:
        title_and_type = f"{title} (Movie)"
    if synopsis == "":
        synopsis = ""
    else:
        synopsis = f'\nSynopsis: {synopsis}\n{providers}'

    event = {
        'summary': title_and_type,
        'description': f'{region} Date {synopsis}',
        'start': {
            'date': datetime.strptime(release_date, '%Y-%m-%d').strftime("%Y-%m-%d"),
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'date': (datetime.strptime(release_date, '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d"),
            'timeZone': 'Europe/Paris',
        },
        'source': {
            'url': f"https://www.themoviedb.org/{type_show}/{ID}",
            'title': 'TMDB Page'
        },
        'transparency': 'transparent'
    }

    # Search for events with the same title
    events_result = service.events().list(calendarId=calendarId, q=title_and_type).execute()
    events = events_result.get('items', [])

    if not events:
        try:
            event = service.events().insert(calendarId=calendarId, body=event).execute()
            #print ('Event created: %s' % (event.get('htmlLink')))
            print('Event created')
        except HttpError as error:
            print('An error occurred' % error)
    else:
        # If one or more events were found with the same title, update the first event
        event_id = events[0]['id']
        try:
            event = service.events().update(calendarId=calendarId, eventId=event_id, body=event).execute()
            #print('Event updated: %s' % (event.get('htmlLink')))
            print('Event updated')
        except HttpError as error:
            print('An error occurred' % error)

if __name__ == '__main__':
    main()
