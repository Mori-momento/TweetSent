import os
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for
from transformers import pipeline
from collections import Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages

# --- Configuration ---
EXCEL_FILE_PATH = 'your_tweets.xlsx'
DEFAULT_TWEET_COUNT = 10
MIN_TWEET_COUNT = 1

# --- Sentiment Analysis Setup ---
try:
    # Load a pre-trained sentiment analysis pipeline from Hugging Face Transformers
    # You might need to install PyTorch or TensorFlow: pip install torch or pip install tensorflow
    # pip install transformers pandas openpyxl Flask
    sentiment_pipeline = pipeline('sentiment-analysis')
    logging.info("Sentiment analysis pipeline loaded successfully.")
except Exception as e:
    logging.error(f"Error loading sentiment analysis pipeline: {e}")
    # Fallback or exit if the pipeline is critical and cannot load
    sentiment_pipeline = None

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using the pre-loaded pipeline.
    Maps standard labels (POSITIVE/NEGATIVE) to Positive/Negative/Neutral.
    """
    if not sentiment_pipeline:
        return "Neutral" # Or handle error appropriately

    try:
        # The pipeline returns a list of dictionaries, e.g., [{'label': 'POSITIVE', 'score': 0.99...}]
        result = sentiment_pipeline(text)[0]
        label = result['label']

        # Map labels - adjust if your chosen model uses different labels
        if 'POSITIVE' in label.upper():
            return "Positive"
        elif 'NEGATIVE' in label.upper():
            return "Negative"
        else:
            # Treat other labels or low confidence scores (if applicable) as Neutral
            # This basic mapping assumes models primarily output POSITIVE/NEGATIVE
            return "Neutral"
    except Exception as e:
        logging.error(f"Error during sentiment analysis for text '{text[:50]}...': {e}")
        return "Neutral" # Default to Neutral on error

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the homepage: displays the form and processes submissions.
    """
    if request.method == 'POST':
        hashtag = request.form.get('hashtag', '').strip()
        n_str = request.form.get('n', str(DEFAULT_TWEET_COUNT)).strip()

        # --- Input Validation ---
        if not hashtag:
            flash('Error: Hashtag cannot be empty.', 'error')
            return render_template('index.html', default_n=DEFAULT_TWEET_COUNT, min_n=MIN_TWEET_COUNT)

        # Ensure hashtag starts with '#' if not already present
        if not hashtag.startswith('#'):
            hashtag = '#' + hashtag

        try:
            n = int(n_str)
            if n < MIN_TWEET_COUNT:
                flash(f'Error: Number of tweets must be at least {MIN_TWEET_COUNT}.', 'error')
                return render_template('index.html', default_n=DEFAULT_TWEET_COUNT, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)
        except ValueError:
            flash('Error: Invalid input for number of tweets. Please enter an integer.', 'error')
            return render_template('index.html', default_n=DEFAULT_TWEET_COUNT, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)

        # --- Data Loading and Processing ---
        try:
            df = pd.read_excel(EXCEL_FILE_PATH)
            logging.info(f"Successfully read Excel file: {EXCEL_FILE_PATH}")

            if hashtag not in df.columns:
                flash(f'Error: Hashtag "{hashtag}" not found in the Excel file.', 'error')
                return render_template('index.html', default_n=n, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)

            # Get the first 'n' non-empty tweets for the hashtag
            tweets = df[hashtag].dropna().astype(str).head(n).tolist()

            if not tweets:
                flash(f'No tweets found for hashtag "{hashtag}" or the column is empty.', 'error')
                return render_template('index.html', default_n=n, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)

            # --- Perform Sentiment Analysis ---
            if not sentiment_pipeline:
                 flash('Error: Sentiment analysis model could not be loaded. Cannot perform analysis.', 'error')
                 return render_template('index.html', default_n=n, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)

            sentiments = [analyze_sentiment(tweet) for tweet in tweets]
            sentiment_counts = Counter(sentiments)
            total_analyzed = len(tweets)

            # Calculate percentages
            results = {
                'hashtag': hashtag,
                'total_analyzed': total_analyzed,
                'positive_pct': round((sentiment_counts.get('Positive', 0) / total_analyzed) * 100, 2) if total_analyzed > 0 else 0,
                'negative_pct': round((sentiment_counts.get('Negative', 0) / total_analyzed) * 100, 2) if total_analyzed > 0 else 0,
                'neutral_pct': round((sentiment_counts.get('Neutral', 0) / total_analyzed) * 100, 2) if total_analyzed > 0 else 0,
            }

            # Redirect to results page (or render directly)
            # Using redirect helps prevent form resubmission on refresh
            # We'll pass data via query parameters for simplicity here
            return redirect(url_for('show_results', **results))

        except FileNotFoundError:
            logging.error(f"Error: Excel file not found at {EXCEL_FILE_PATH}")
            flash(f'Error: Data file "{EXCEL_FILE_PATH}" not found.', 'error')
            return render_template('index.html', default_n=n, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            flash(f'An unexpected error occurred: {e}', 'error')
            return render_template('index.html', default_n=n, min_n=MIN_TWEET_COUNT, submitted_hashtag=hashtag)

    # --- GET Request ---
    # Display the initial form
    return render_template('index.html', default_n=DEFAULT_TWEET_COUNT, min_n=MIN_TWEET_COUNT)

@app.route('/results')
def show_results():
    """
    Displays the sentiment analysis results passed via query parameters.
    """
    # Retrieve results from query parameters
    results = {
        'hashtag': request.args.get('hashtag', 'N/A'),
        'total_analyzed': request.args.get('total_analyzed', 0, type=int),
        'positive_pct': request.args.get('positive_pct', 0.0, type=float),
        'negative_pct': request.args.get('negative_pct', 0.0, type=float),
        'neutral_pct': request.args.get('neutral_pct', 0.0, type=float),
    }
    return render_template('results.html', results=results)

# --- Run the App ---
if __name__ == '__main__':
    # Make sure the transformers library and a backend (torch/tensorflow) are installed
    # pip install Flask pandas openpyxl transformers torch (or tensorflow)
    if not sentiment_pipeline:
        print("CRITICAL ERROR: Sentiment analysis pipeline failed to load. Exiting.")
    else:
        # Use host='0.0.0.0' to make it accessible on the network
        app.run(debug=True, host='0.0.0.0', port=5000)