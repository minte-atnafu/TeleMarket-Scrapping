import pandas as pd
from nltk.tokenize import word_tokenize
from text_unidecode import unidecode
import nltk
import re

# Download required NLTK data
nltk.download('punkt')

# Load the cleaned data
data = pd.read_csv("cleaned_data.csv")

# Handle missing values
data.fillna("Unknown", inplace=True)

# Remove duplicates
data.drop_duplicates(inplace=True)

# Normalize text (e.g., Amharic)
data['Message'] = data['Message'].apply(lambda x: unidecode(x) if isinstance(x, str) else x)

# Remove unwanted symbols in the Message column
data['Message'] = data['Message'].str.replace(r'[^\w\s]', '', regex=True)

# Special cleaning for the `Channel Title` column (remove symbols like 📱 for Phone hub📱)
data['Channel Title'] = data['Channel Title'].str.replace("📱", "", regex=False)

# Remove the ® symbol from the `Channel Title` column
data['Channel Title'] = data['Channel Title'].str.replace('®', '', regex=False)

# Function to remove unwanted patterns in the Message column
def remove_unwanted_text(text):
    if isinstance(text, str):
        # Define the regex pattern for unwanted text
        pattern = r"(price|birr)\s*sww\s*2844\s*(\n|\s)*httpstmesamcomptech"
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    return text

# Apply the cleaning function only for rows where `Channel Title` is "Sami Tech"
data.loc[data['Channel Title'] == 'Sami Tech', 'Message'] = \
    data.loc[data['Channel Title'] == 'Sami Tech', 'Message'].apply(remove_unwanted_text)

# Tokenize text in the Message column
data['Tokens'] = data['Message'].apply(lambda x: word_tokenize(x) if isinstance(x, str) else [])

# Remove rows where the 'Message' column is "Unknown"
data = data[data['Message'] != 'Unknown']

# Save cleaned data back to the file
data.to_csv("cleaned_data.csv", index=False)

print("Data cleaning complete! Cleaned data saved to cleaned_data.csv.")
