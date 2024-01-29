import pickle
from transformers import AutoTokenizer, pipeline

# Function to load the model from a pickle file
def load_model_from_pickle(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Load your saved model
model_artifact_path = 'model_artifact_llm_news.pkl'  # Adjust path as needed
lm_model = load_model_from_pickle(model_artifact_path)

# Set up the tokenizer and pipeline for text generation
model_id = "databricks/dolly-v2-3b"  # Adjust model ID as needed
tokenizer = AutoTokenizer.from_pretrained(model_id)
pipe = pipeline("text-generation", model=lm_model, tokenizer=tokenizer, max_new_tokens=256)

# Test the model with a prompt
test_prompt = "What are the latest trends in technology?"
lm_response = pipe(test_prompt)
print(lm_response[0]["generated_text"])
