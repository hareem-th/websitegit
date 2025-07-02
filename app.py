import json 
from flask import Flask, render_template, request, redirect, url_for, session #flask to created web application, to render html templates, requested to handle to form applications, url;to redirect user btw routes
import os #work with files path

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load quiz data from JSON files
def load_json(file_name):
    file_path = os.path.join(os.getcwd(), 'data', file_name) #returns the current wrking directory, subdirectory JSON files are stored.
    with open(file_path, 'r') as f: 
        return json.load(f) 

# Route for the homepage
@app.route('/') 
def index(): 
    session.clear() 
    return render_template('index.html') 

# Meme Quiz Route
@app.route('/meme_quiz', methods=['GET', 'POST']) #user visit the page,  
def meme_quiz():  #data is stored in quiz_data and will be used to show questions
    quiz_data = load_json('meme.json')

    # Initialize session variables, Set kro session for the quiz agr the user's first time starting.
    if 'current_question' not in session:
        session['current_question'] = 0 #Keeps track konse  question user pe hai
        session['answers'] = []

    # Check if quiz is completed
    if session['current_question'] >= len(quiz_data): 
        return redirect(url_for('meme_result')) 

    # Handle POST request
    if request.method == 'POST':  
        answer = request.form.get('answer')  # Get selected answer, Retrieves the user’s selected answer from the submitted form.
        if answer:
            session['answers'].append(answer) #answer added to session['answers']
            session['current_question'] += 1  #increase kr rhe by 1 to move to the next question
        return redirect(url_for('meme_quiz')) 

    # Get current question
    current_question = quiz_data[session['current_question']] #quiz data into current questions
    return render_template('quiz.html', current_question=current_question, quiz_type='Meme')

@app.route('/meme_result')
def meme_result():
    user_answers = session.get('answers', []) #Retrieves the answers during the quiz user ne diye.
    quiz_data = load_json('meme.json') # quiz data loaded calculate/display result on user's answers.

    # Map personality types to their corresponding images
    result_to_image = {
        "You're just a chill guy.": "chillguy.jpg",
        "Expects an easy day, failed.": "failed.jpg",
        "Main character energy? Always ON.": "main_character.jpg"
    }

    # Determine personality type based on user answers
    result_count = {} #Initializes a khali dictionary to store the count of each result.
    for answer in user_answers: 
        for question in quiz_data: 
            for option_text, result in question['options'].items(): 
                if answer == option_text: #Compares the user’s answer (answer) with the current option text 
                    result_count[result] = result_count.get(result, 0) + 1

    # Debug: Print result_count to see how answers are being counted
    print(f"Result Count: {result_count}") 

    # Get the personality type with the highest count
    personality_type = max(result_count, key=result_count.get, default="Could not guess your personality")
    
    # Debug: Print personality_type to confirm it’s being set correctly
    print(f"Personality Type: {personality_type}")

    image = result_to_image.get(personality_type, "default.png")  # Map personality type to image

    session.clear()  # Clear session after results
    return render_template('meme_result.html', personality_type=personality_type, image=image)


# General Quiz Route
@app.route('/general_quiz', methods=['GET', 'POST']) 
def general_quiz(): 
    quiz_data = load_json('general.json') #Starts the function that will handle requests to the /general_quiz route.
#initialize for the user
    if 'current_question' not in session: #Checks if current_question exists in the session
        session['current_question'] = 0 #If not, it initializes
        session['score'] = 0
#Ends the quiz when all questions have been answered.
    if session['current_question'] >= len(quiz_data): #Compares the current_question with total num of questions
        return redirect(url_for('general_result'))

    if request.method == 'POST':
        answer = request.form.get('answer') # Retrieves the user’s selected answer from the submitted form.
        correct_answer = quiz_data[session['current_question']]['correct'] #Compares the user’s answer (answer) with correct answer from  current question
        if answer and answer == correct_answer: # written this way to handle two important scenarios:
            session['score'] += 1 #increases score if true
        session['current_question'] += 1 #increases question if true
        return redirect(url_for('general_quiz')) 

    current_question = quiz_data[session['current_question']] #This is a number (starting at 0) that tracks user 
    return render_template('quiz.html', current_question=current_question, quiz_type='General') #returns the questions to quiz.html

@app.route('/general_result') #route for the URL /general_result.
def general_result():
    score = session.get('score', 0) #Retrieves user's score from session. If session['score'] exists, uses value. If session['score'] is missing defaults 0.
    total_questions = len(load_json('general.json')) #Counts the total number of questions in the quiz 
    session.clear()  # Clear session after results
    return render_template('general_result.html', score=score, total_questions=total_questions) #The user’s final score.The total number of questions in the quiz.

# Apocalypse Quiz Route
@app.route('/apocalypse_quiz', methods=['GET', 'POST']) # route for the URL /apocalypse_quiz.
def apocalypse_quiz():
    quiz_data = load_json('apocalypse.json')

    if 'current_question' not in session:
        session['current_question'] = 0 #Start the user at the first questio
        session['scare_factor'] = 0 #Start the "scare factor" score at zero

    if session['current_question'] >= len(quiz_data): #racks the question number the user is currently answ
        return redirect(url_for('apocalypse_result'))

    if request.method == 'POST': #This block runs when the user submits their answer
        answer = request.form.get('answer') #Retrieves the answer the user selected from the form.
        if answer in quiz_data[session['current_question']]['scare_points']: #quiz data loading json, session giving current question index of user
            scare_points = int(quiz_data[session['current_question']]['scare_points'][answer]) #indicate how challenging or nerve-wracking the question is under time pressure.
            session['scare_factor'] += scare_points #links each answer to a scare point value.
        session['current_question'] += 1
        return redirect(url_for('apocalypse_quiz'))

    current_question = quiz_data[session['current_question']]
    return render_template('quiz.html', current_question=current_question, quiz_type='Apocalypse')

@app.route('/apocalypse_result')
def apocalypse_result():
    scare_factor = session.get('scare_factor', 0)
    session.clear()  # Clear session after results

    # Define scare messages and survival tips based on score ranges
    if scare_factor < 20:
        scare_message = "You kept your cool and stayed safe!"
        survival_tips = [
            "Continue to avoid unnecessary risks.",
            "Stay vigilant and plan your moves carefully.",
            "Keep your resources stocked and prioritize safety."
        ]
    elif 20 <= scare_factor < 50:
        scare_message = "You had a few close calls but managed to pull through."
        survival_tips = [
            "Consider balancing bravery with caution.",
            "Stay prepared for unexpected situations.",
            "Work on your decision-making under pressure."
        ]
    else:
        scare_message = "Your actions were daring, but you took significant risks!"
        survival_tips = [
            "Reassess your strategy to avoid unnecessary dangers.",
            "Learn to prioritize survival over boldness.",
            "Build alliances to improve your chances in high-risk scenarios."
        ]

    return render_template( #display the result page for the "Apocalypse Quiz" with dynamic content
        'apocalypse_result.html',
        scare_factor=scare_factor, #Represents the user’s "scare factor" score from the quiz.
        scare_message=scare_message,
        survival_tips=survival_tips
    )


if __name__ == '__main__':
    app.run(debug=True)