import pandas as pd

# Sample data for the Excel file
data = {
    '#TechNews': [
        "Just got the new XYZ phone, the camera is amazing!", # Positive
        "This software update is incredibly buggy, very frustrating.", # Negative
        "Apple announced their quarterly earnings today.", # Neutral
        "Loving the new features in the latest OS release.", # Positive
        "My laptop battery life seems worse after the update.", # Negative
        "Rumors suggest a new gaming console is coming soon.", # Neutral
        "The AI conference keynote was quite insightful.", # Positive
        "Another data breach reported... getting tired of this.", # Negative
        "Cloud computing costs are projected to increase next year.", # Neutral
        "This new programming language looks promising.", # Positive
        "The website redesign is confusing and hard to navigate.", # Negative
        "Stock prices for tech companies were mixed today.", # Neutral
        "Finally, a foldable phone that feels durable!", # Positive
        "Why is customer support so unresponsive?", # Negative
    ],
    '#MovieReview': [
        "Just watched 'Galaxy Quest 2', absolutely hilarious and heartwarming!", # Positive
        "That new horror movie was a complete waste of time, so predictable.", # Negative
        "The documentary provided a detailed look at historical events.", # Neutral
        "The acting in 'Sunset Boulevard Revisited' was phenomenal.", # Positive
        "I fell asleep during the movie, it was that boring.", # Negative
        "The film's runtime is approximately 2 hours and 15 minutes.", # Neutral
        "Visually stunning, the cinematography was breathtaking.", # Positive
        "Terrible plot holes and wooden dialogue ruined it for me.", # Negative
        "The movie is based on a best-selling novel.", # Neutral
        "A must-watch for fans of the genre!", # Positive
        "Disappointed by the sequel, didn't live up to the original.", # Negative
        "The soundtrack features several popular artists.", # Neutral
    ],
    '#PythonTips': [
        "List comprehensions make Python code so much cleaner!", # Positive
        "Debugging async code can be a real headache sometimes.", # Negative
        "Python 3.12 introduced several new features.", # Neutral
        "Using virtual environments is crucial for managing dependencies.", # Positive
        "The Global Interpreter Lock (GIL) limits true parallelism in CPython.", # Negative (often seen as a limitation)
        "Pandas is great for data manipulation.", # Positive
        "Remember to handle potential exceptions with try-except blocks.", # Neutral/Positive (good practice)
        "Type hints improve code readability and maintainability.", # Positive
        "Setting up complex project structures can be tricky.", # Negative
        "The official Python documentation is very comprehensive.", # Neutral/Positive
    ]
}

# Find the maximum length of the lists to create a balanced DataFrame
max_len = 0
for key in data:
    if len(data[key]) > max_len:
        max_len = len(data[key])

# Pad shorter lists with None (which will become empty cells in Excel)
for key in data:
    data[key].extend([None] * (max_len - len(data[key])))

# Create DataFrame
df = pd.DataFrame(data)

# Define the output file path
excel_file_path = 'your_tweets.xlsx'

try:
    # Write the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)
    print(f"Successfully created sample data file: {excel_file_path}")
except Exception as e:
    print(f"Error writing Excel file: {e}")
