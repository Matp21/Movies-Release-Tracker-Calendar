# Movie and TV Show Release Tracker

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Movie and TV Show Release Tracker is a Python script that allows you to track movie and TV show releases from specific companies and add them to a Google Calendar. It retrieves data from the TMDB API, including release dates, posters, synopses, and watch providers, and integrates with Google Calendar using the Google Calendar API.

## Features

- Track movie and TV show releases from one or more companies and added them to your Google Calendar.
- Retrieve release dates, synopses, and watch providers for each title.
- Supports multiple regions and languages for data retrieval.

## Prerequisites

Before running the script, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- The required Python packages installed. You can install them by running the following command: `pip install -r requirements.txt`

- Obtain a TMDB API key. You can create an account and get an API key from the [TMDB website](https://www.themoviedb.org/documentation/api).
- Create a Google Calendar and obtain the necessary credentials for the Google Calendar API. Follow the [Google Calendar API documentation](https://developers.google.com/calendar/quickstart/python) to set up your project and generate credentials (put the file "credentials.json" in the same place as the script).

## Configuration

Before running the script, you need to configure the following:

- Set your TMDB API key: Replace `api_key = "YOUR_TMDB_API_KEY"` in the script with your actual TMDB API key.
- Set your Google Calendar ID: Replace `calendarId = 'YOUR_GOOGLE_CALENDAR_ID'` in the script with the ID of your Google Calendar.
- Obtain the production company IDs for the movies or TV shows you want to track. These IDs can be found in the JSON file named ["production_company_ids.json"](https://github.com/Matp21/Movies-Release-Tracker/production_company_ids.json). Replace them in `companies_id = ["YOUR_COMPANIES_ID_HERE"]`
- Set the language in the script to specify the desired language format. Modify the variable `language` and set it to the desired language code (e.g., "fr-FR", "us-US", etc.).
- Set the principal region in the script to specify the primary region for retrieving release dates and watch providers. Modify the variable `first_region` and set it to the desired region code (e.g., "FR", "US", etc.).
- Set the secondary region in the script to specify the backup region for retrieving release dates and watch providers. Modify the variable `second_region` and set it to the desired region code (e.g., "FR", "US", etc.).


## Usage

To use the script:

1. Clone this repository to your local machine or download the script file.

2. Install the required dependencies by running: `pip install -r requirements.txt`

3. Configure the script by following the "Configuration" section mentioned above.

4. Run the script: `python movies_release_tracker.py` or run `run.bat`

The script will retrieve data for the specified companies, check for upcoming releases, and add events to your Google Calendar.

## Contributing

Contributions to the Movie and TV Show Release Tracker are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The Movie Database (TMDB) for providing the movie and TV show data API.
- Google Calendar API for enabling calendar integration.

## Contact

If you have any questions or suggestions, please feel free to reach out to us.

## Disclaimer

This script is provided as-is with no warranty or guarantee. Use it at your own risk.

---

Feel free to enhance and customize the README file based on your specific requirements. Provide clear instructions on how to set up and use the script, and mention any additional details or considerations that may be relevant.


