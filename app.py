from flask import Flask, render_template, request, jsonify
import spacy
import random

app = Flask(__name__)

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Given paragraph
paragraph = """
Sharlz is a revolutionary clothing brand that is set to transform the fashion industry. 
With a focus on generation Z, Sharlz aims to provide an immersive shopping experience through its upcoming virtual try-on feature. 
The brand recognizes the need for personalized shopping experiences and aims to deliver just that through its advanced technology. 
Sharlz also offers exquisite packaging, ensuring that the customer's shopping experience doesn't end after the purchase. 
With a wide range of trendy and comfortable clothing options, Sharlz is the go-to brand for the stylish and tech-savvy generation Z. 
With our upcoming feature, Try on clothes virtually and have them delivered in style with Sharlz.
"""

# Process the paragraph with spaCy
doc = nlp(paragraph)

# Sample greetings for dynamic responses
greetings = ["Hello!", "Hi there!", "Greetings!", "Hey!", "Welcome!"]

# Dictionary to map questions to relevant information
question_mapping = {
    "focus": "Sharlz focuses on generation Z and aims to provide an immersive shopping experience through virtual try-on technology.",
    "packaging": "Sharlz offers exquisite packaging to enhance the overall customer experience.",
    "clothing options": "Sharlz provides a wide range of trendy and comfortable clothing options for the stylish and tech-savvy generation Z.",
    "virtual try on": "Sharlz's upcoming feature allows customers to try on clothes virtually and have them delivered in style."
}

# Dictionary to map follow-up responses
follow_up_mapping = {
    "really?": "Yes. we do have that. {response}",
    "wow!": "We're glad you're excited! {response}",
    # Add more follow-up responses as needed
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']

    answer = answer_question(question)

    return jsonify({'answer': answer})

def answer_question(question):
    # Default answer
    answer = "I'm sorry, I don't have information on that."

    # Check if the question contains key phrases from the mapping
    for key_phrase, response in question_mapping.items():
        if key_phrase in question.lower():
            answer = f"{random.choice(greetings)} {response}"
            break

    # Check if the question is a follow-up response
    for follow_up, response_template in follow_up_mapping.items():
        if follow_up in question.lower():
            initial_response = question_mapping.get(follow_up.replace('?', '').strip(), "")
            answer = f"{random.choice(greetings)} {response_template.format(response=initial_response)}"
            break

    return f"Sharlz's Bot: {answer}"

if __name__ == '__main__':
    app.run(debug=True)
