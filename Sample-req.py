import requests
import base64

# Define the API endpoint
url = "http://localhost:5000/v1/sentiment"

# Define the username and password
username = "Yoshi"
password = "4237"
auth_header = base64.b64encode(f"{username}:{password}".encode()).decode("utf-8")

# Define the sentence for sentiment analysis
sentence = "This is a sample sentence."

# Make the POST request
response = requests.post(
    url,
    headers={"Content-Type": "application/json", "Authorization": f"Basic {auth_header}"},
    json={"sentence": sentence}
)

# Print the response
print(response.json())
