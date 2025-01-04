import pandas as pd
import re

# Function to clean unwanted text
def remove_unwanted_text(text):
    if isinstance(text, str):
        # Refined regex to specifically target the unwanted text
        patterns = [
            r"Price\s*sww2844\s*Call\s*httpstmesamcomptech",  # First unwanted pattern
            r"birr\s*sww2844\s*httpstmesamcomptech"          # New unwanted pattern
        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
        
        # Remove any extra whitespace after cleaning
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    return text


# Load the data
data = pd.read_csv("combined_features.csv")  # Adjust the file name if necessary

# Apply cleaning function only to rows with 'Channel Title' == 'Sami Tech'
data.loc[data['Channel Title'] == 'Sami Tech', 'Specifications'] = (
    data.loc[data['Channel Title'] == 'Sami Tech', 'Specifications']
    .apply(remove_unwanted_text)
)

# Save cleaned data to a new CSV file
data.to_csv("cleaned_featured_data.csv", index=False)

print("Unwanted text removed for 'Sami Tech'! Cleaned data saved to cleaned_feature_engineered_data.csv.")
