import requests
import json

# Your OpenAI API key
api_key = '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'

# API endpoint for GPT-3 completion
api_url = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions'  # Adjust the engine and endpoint as needed

# Prompt for the text completion
prompt = 'Once upon a time'

# Parameters for the API request
data = {
    'prompt': prompt,
    'max_tokens': 50,  # You can adjust this value to control the length of the completion
}

# Headers with the API key
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

try:
    # Send a POST request to the API
    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    # Check if the response status code indicates success (2xx)
    if response.status_code // 100 == 2:
        result = response.json()
        completion_text = result['choices'][0]['text']
        print('Generated completion:')
        print(completion_text)
    else:
        print(f'API request failed with status code: {response.status_code}')
        print('Error Message:')
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {str(e)}')