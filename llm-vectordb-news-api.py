from flask import Flask, request, jsonify
import pickle
from transformers import AutoTokenizer, pipeline

app = Flask(__name__)

# Load the model from a pickle file
def load_model_from_pickle(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Set up the tokenizer and pipeline for text generation
def setup_pipeline(model):
    model_id = "databricks/dolly-v2-3b"  # Adjust model ID as needed
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=256)
    return pipe

# Load the saved model
model_artifact_path = 'model_artifact_llm_news.pkl'  # Adjust path as needed
lm_model = load_model_from_pickle(model_artifact_path)
pipe = setup_pipeline(lm_model)

# Function to handle chat input and return response
def get_model_response(chat_input):
    lm_response = pipe(chat_input)
    return lm_response[0]['generated_text']

# Flask endpoint for Q&A chat
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    chat_input = data['message']
    response = get_model_response(chat_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
