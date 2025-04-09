# TweetSent

TweetSent is a web application for analyzing tweets and visualizing the results. It allows you to upload tweet data, process it, and view the analysis through a user-friendly interface.

## Features

- Upload and analyze tweets
- View results in a web interface
- Sample data generation script included

## Requirements

- Python 3.7+
- Required packages listed in `requirements.txt`

## Setup

1. **Clone the repository**

```
git clone <repository_url>
cd TweetSent
```

2. **Create a virtual environment (optional but recommended)**

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```
pip install -r requirements.txt
```

4. **(Optional) Generate sample data**

```
python create_sample_data.py
```

## Running the App

```
python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000/`.

## Project Structure

- `app.py` - Main Flask application
- `create_sample_data.py` - Script to generate sample tweet data
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `your_tweets.xlsx` - Example tweet data file

## License

This project is licensed under the MIT License.
