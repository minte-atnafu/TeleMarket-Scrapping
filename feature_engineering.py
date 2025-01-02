import pandas as pd
import re

# Load the cleaned data
data = pd.read_csv("cleaned_data.csv")

# Define feature extraction functions for EthioBrand
def process_ethio_brand(messages):
    features = []
    for message in messages:
        # Extract brand name (before 'Size')
        brand = re.search(r"([A-Za-z]+(?:\s[A-Za-z]+)*)\s*SD?", message)
        
        # Extract size values (remove the word 'Size' and format the numbers)
        size = re.search(r"Size\s*([\d\s]+)", message)
        
        # Extract price and add 'birr'
        price = re.search(r"Price\s([\d,]+)\s*birr", message)
        
        # Format the size properly (with spaces between numbers)
        size_values = size.group(1).strip().replace(" ", " ") if size else None
        
        features.append({
            "Brand": brand.group(1) if brand else None,
            "Size": size_values,  # Size with spaces between numbers
            "Price": price.group(1) + " birr" if price else None,
        })
    return pd.DataFrame(features)

# Define other channel extraction functions (unchanged)
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
    features = []
    for message in messages:
        # Debugging: Print the message being processed
        print(f"Processing message: {message}")

        # Extract price (ensure it follows "PRICE") and append "birr"
        price_match = re.search(r"PRICE\s+([\d,]+)", message, re.IGNORECASE)
        if price_match:
            price_info = price_match.group(1).replace(",", "") + " birr"
            # Remove the price from the message
            message = re.sub(r"PRICE\s+[\d,]+", "", message, flags=re.IGNORECASE)
        else:
            price_info = None

        # Remove leading/trailing spaces after modification
        message = message.strip()

        # Extract phone numbers
        phone_numbers = re.findall(r"\b\d{9,10}\b", message)
        phone_numbers_info = ", ".join(phone_numbers) if phone_numbers else None

        # Remove phone numbers from the message
        message = re.sub(r"\b\d{9,10}\b", "", message).strip()

        # Debugging: Print cleaned specifications
        print(f"Cleaned message: {message}")

        features.append({
            "Specifications": message,  # Remaining text after removing price and phone numbers
            "Price": price_info,
            "Phone Numbers": phone_numbers_info,
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

# Replace 'Message' column with the new features for EthioBrand channel
ethio_brand_data = ethio_brand_data.drop(columns=['Message']).reset_index(drop=True)
ethio_brand_data = pd.concat([ethio_brand_data, ethio_brand_features], axis=1)

# Replace 'Message' column with the new features for Phone Hub channel
phone_hub_data = phone_hub_data.drop(columns=['Message']).reset_index(drop=True)
phone_hub_data = pd.concat([phone_hub_data, phone_hub_features], axis=1)

# Replace 'Message' column with the new features for Sami Tech channel
sami_tech_data = sami_tech_data.drop(columns=['Message']).reset_index(drop=True)
sami_tech_data = pd.concat([sami_tech_data, sami_tech_features], axis=1)

# Combine data from all channels into one DataFrame
combined_data = pd.concat([ethio_brand_data, phone_hub_data, sami_tech_data], axis=0, ignore_index=True)

# Save the combined data into a single CSV file
combined_data.to_csv("combined_features.csv", index=False)

print("Feature engineering complete! Processed data saved as combined_features.csv.")
