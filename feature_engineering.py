import pandas as pd
import re

# Load the cleaned data
data = pd.read_csv("cleaned_data.csv")

# Define feature extraction functions
def process_ethio_brand(messages):
    features = []
    for message in messages:
        size = re.search(r"Size\s([\d\s]+)", message)
        price = re.search(r"Price\s([\d,]+)", message)
        features.append({
            "Size": size.group(1) if size else None,
            "Price": price.group(1) if price else None,
        })
    return pd.DataFrame(features)

def process_phone_hub(messages):
    features = []
    for message in messages:
        model = re.search(r"(Samsung|iPhone|Huawei|Xiaomi).*", message, re.IGNORECASE)
        price = re.search(r"Price\s([\d,]+)", message)
        features.append({
            "Model": model.group(0) if model else None,
            "Price": price.group(1) if price else None,
        })
    return pd.DataFrame(features)

def process_sami_tech(messages):
    # Example: Extract tech specs or prices (modify as needed)
    features = []
    for message in messages:
        specs = re.search(r"(RAM|Storage|Processor).*", message, re.IGNORECASE)
        price = re.search(r"Price\s([\d,]+)", message)
        features.append({
            "Specs": specs.group(0) if specs else None,
            "Price": price.group(1) if price else None,
        })
    return pd.DataFrame(features)

# Filter data by channel and apply feature engineering
ethio_brand_data = data[data['Channel Title'] == 'EthioBrand']
phone_hub_data = data[data['Channel Title'] == 'Phone hub']
sami_tech_data = data[data['Channel Title'] == 'Sami Tech']

# Apply feature extraction functions to each channel
ethio_brand_features = process_ethio_brand(ethio_brand_data['Message'])
phone_hub_features = process_phone_hub(phone_hub_data['Message'])
sami_tech_features = process_sami_tech(sami_tech_data['Message'])

# Combine features back into original data
ethio_brand_data = pd.concat([ethio_brand_data.reset_index(drop=True), ethio_brand_features], axis=1)
phone_hub_data = pd.concat([phone_hub_data.reset_index(drop=True), phone_hub_features], axis=1)
sami_tech_data = pd.concat([sami_tech_data.reset_index(drop=True), sami_tech_features], axis=1)

# Combine data from all channels into one DataFrame
combined_data = pd.concat([ethio_brand_data, phone_hub_data, sami_tech_data], axis=0, ignore_index=True)

# Save the combined data into a single CSV file
combined_data.to_csv("combined_features.csv", index=False)

print("Feature engineering complete! Processed data saved as combined_features.csv.")
