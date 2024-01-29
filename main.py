"""This script launches the Flask server and renders the portfolio page."""
from flask import Flask, render_template, request
from flask_recaptcha import ReCaptcha  # Import ReCaptcha object
from flask_compress import Compress
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
import datetime as dt

from flask import Flask, request, jsonify
import pickle
from transformers import AutoTokenizer, pipeline

OWN_EMAIL = os.getenv('mail')
OWN_PASSWORD = os.getenv('pass')


app = Flask(__name__)
compress = Compress()
compress.init_app(app)
app.config['RECAPTCHA_SITE_KEY'] = \
    os.getenv('key_site')  # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = \
    os.getenv('key_secret')  # <-- Add your secret key
recaptcha = ReCaptcha(app)  # Create a ReCaptcha object


@app.route("/")
def home():
    """Render index.html template."""
    current_year = dt.datetime.now().year
    return render_template('index.html', year=current_year)


@app.route("/submit", methods=["POST"])
def receive_data():
    """Receive the input from the contact section."""
    if request.method == "POST":
        if recaptcha.verify():
            name = request.form["name"]
            mail = request.form["mail"]
            phone = request.form["phone"]
            message = request.form["message"]
            send_email(name, mail, phone, message)
            return render_template('submission.html')
        else:
            return render_template('index.html')


def send_email(name, email, phone, message):
    """Send email to my personal account with smtp."""
    email_message = \
        f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    msg = MIMEMultipart()
    msg['To'] = OWN_EMAIL
    msg['Subject'] = 'Contact Portfolio'
    msg.attach(MIMEText(email_message, "plain"))
    text = msg.as_string()
    with smtplib.SMTP(host='smtp-mail.outlook.com', port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, text)

# Global variables for model and pipeline
global llm_news_model
global pipe
pipe = None
llm_news_model = None

@app.route('/chat_news')
def chat_interface():
    return render_template('llm_model_news.html')

# Endpoint to load the model
@app.route('/load_llm_news_model', methods=['GET'])
def load_model():
    global llm_news_model, pipe
    model_artifact_path = 'model_artifact_llm_news.pkl'  # Adjust path as needed

    # Load the model from a pickle file
    with open(model_artifact_path, 'rb') as file:
        llm_news_model = pickle.load(file)

    # Set up the tokenizer and pipeline for text generation
    model_id = "databricks/dolly-v2-3b"  # Adjust model ID as needed
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    pipe = pipeline("text-generation", model=llm_news_model, tokenizer=tokenizer, max_new_tokens=256)

    return jsonify({"message": "Model loaded successfully"})

# Function to handle chat input and return response
@app.route('/chat_llm_news', methods=['POST'])
def get_model_response():
    global pipe
    data = request.json
    chat_input = data['message']
    lm_response = pipe(chat_input)
    return jsonify({'response': lm_response[0]['generated_text']})

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['RECAPTCHA_SIZE'] = 'compact'
    app.run(port=5000, host='0.0.0.0', debug=True)
