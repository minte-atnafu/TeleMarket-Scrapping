import pandas as pd
import re
from text_unidecode import unidecode

# Load the data
data = pd.read_csv("combined_features.csv")  # Make sure to load the correct file

# Data Cleaning Function
def remove_unwanted_text(text):
    if isinstance(text, str):
        # Refined regex pattern for variations
        pattern = r"(price|birr|call)\s*sww2844\s*(\n|\s)*httpstmesamcomptech"
        cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
        
        # Clean up extra whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text
    return text

# Apply cleaning function to 'specification' column where 'Channel Title' is 'Sami Tech'
data.loc[data['Channel Title'] == 'Sami Tech', 'Specifications'] = \
    data.loc[data['Channel Title'] == 'Sami Tech', 'Specifications'].apply(remove_unwanted_text)

# Save cleaned data
data.to_csv("cleaned_featured_data.csv", index=False)

print("Data cleaning complete! Cleaned data saved to cleaned_featured_data.csv.")
