import requests

# Specify the necessary parameters
subdomain = "docs"
docId = "nSV5r7CLQCWzKqZCz7qBor"
tableId = "Form2"
api_url = f"https://{subdomain}.getgrist.com/api/docs/{docId}/tables/{tableId}/records"
api_key = "3a00dc02645f6f36f4e1c9449dd4a8529b5e9149"
# Set up the API key for authorization
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Prepare the request body
records = [
    {
        "fields": {"nom": "value1", "prenom": "value2"}
    },
    {
        "fields": {"nom": "value3", "prenom": "value4"}
    }
    # Add more records as needed in the same format
]

data = {
    "records": records
}

# Make the POST request
response = requests.post(api_url, headers=headers, json=data)
# Check the response status
if response.status_code == 200:
    print("Records added successfully!")
else:
    print("Error adding records. Status code:", response.status_code)
    print("Error message:", response.text)