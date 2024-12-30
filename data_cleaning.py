import pandas as pd
from nltk.tokenize import word_tokenize
from text_unidecode import unidecode
import nltk

nltk.download('punkt')

# Load the scraped data
data = pd.read_csv("telegram_data.csv")

# Handle missing values
data.fillna("Unknown", inplace=True)

# Remove duplicates
data.drop_duplicates(inplace=True)

# Normalize text (e.g., Amharic)
data['Message'] = data['Message'].apply(lambda x: unidecode(x) if isinstance(x, str) else x)

# Remove unwanted symbols
data['Message'] = data['Message'].str.replace(r'[^\w\s]', '', regex=True)

# Tokenize text
data['Tokens'] = data['Message'].apply(lambda x: word_tokenize(x) if isinstance(x, str) else [])

# Save cleaned data
data.to_csv("cleaned_data.csv", index=False)

print("Data cleaning complete! Cleaned data saved to cleaned_data.csv.")
