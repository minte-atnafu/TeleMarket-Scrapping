import pandas as pd
import re

# Load the cleaned data
data = pd.read_csv("cleaned_featured_data.csv")

# Define feature extraction for EthioBrand
def process_ethio_brand(data):
    features = []
    for _, row in data.iterrows():
        # Use existing columns directly
        brand = row['Brand'] if 'Brand' in row else None
        size = row['Size'] if 'Size' in row else None
        price = row['Price'] + " birr" if 'Price' in row and pd.notnull(row['Price']) else None
        
        features.append({
            "Brand": brand,
            "Size": size,
            "Price": price,
        })
    return pd.DataFrame(features)

# Define feature extraction for Phone Hub channel
def process_phone_hub(data):
    features = []
    for _, row in data.iterrows():
        # Extract model and specifications from the text data
        model = row['Brand'] if 'Brand' in row else None
        specifications = row['Size'] if 'Size' in row else None
        price = row['Price'] + " birr" if 'Price' in row and pd.notnull(row['Price']) else None

        features.append({
            "Model": model,
            "Specifications": specifications,
            "Price": price,
        })
    return pd.DataFrame(features)

# Define feature extraction for Sami Tech channel
def process_sami_tech(data):
    features = []
    for _, row in data.iterrows():
        # Extract price
        price = row['Price'] + " birr" if 'Price' in row and pd.notnull(row['Price']) else None
        specifications = row['Size'] if 'Size' in row else None
        
        features.append({
            "Specifications": specifications,
            "Price": price,
        })
    return pd.DataFrame(features)

# Filter data by channel and apply feature engineering
ethio_brand_data = data[data['Channel Title'] == 'EthioBrand']
phone_hub_data = data[data['Channel Title'] == 'Phone hub']
sami_tech_data = data[data['Channel Title'] == 'Sami Tech']

# Apply feature extraction functions to each channel
ethio_brand_features = process_ethio_brand(ethio_brand_data)
phone_hub_features = process_phone_hub(phone_hub_data)
sami_tech_features = process_sami_tech(sami_tech_data)

# Replace original columns with processed features
ethio_brand_data = pd.concat([ethio_brand_data.reset_index(drop=True), ethio_brand_features], axis=1)
phone_hub_data = pd.concat([phone_hub_data.reset_index(drop=True), phone_hub_features], axis=1)
sami_tech_data = pd.concat([sami_tech_data.reset_index(drop=True), sami_tech_features], axis=1)

# Combine all processed data
combined_data = pd.concat([ethio_brand_data, phone_hub_data, sami_tech_data], axis=0, ignore_index=True)

# Save the combined data
combined_data.to_csv("cleaned_featured_data.csv", index=False)

print("Feature engineering complete! Processed data saved as combined_features.csv.")
