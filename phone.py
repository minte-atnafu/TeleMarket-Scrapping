import pandas as pd
import re 
# Load the data
data = pd.read_csv("cleaned_featured_data.csv")  # Adjust the file name if necessary

# Function to extract address from the Specifications column
def extract_address(specifications):
    if isinstance(specifications, str):
        # Look for text after "Address"
        match = re.search(r'Address(.+)', specifications)
        if match:
            return match.group(1).strip()  # Extract and remove extra spaces
    return None  # Return None if "Address" is not found

# Apply extraction function to rows with Channel Title == 'Phone hub'
data.loc[data['Channel Title'] == 'Phone hub', 'Address'] = (
    data.loc[data['Channel Title'] == 'Phone hub', 'Specifications']
    .apply(extract_address)
)

# Save the updated data to a new CSV file
data.to_csv("cleaned_featured_data.csv", index=False)

print("Address column added for 'Phone hub'!")
