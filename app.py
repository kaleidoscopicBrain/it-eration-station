from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging

app = Flask(__name__)

# Set a secret key for session management (This should be kept secret in a real application)
app.secret_key = 'your_secret_key_here'

# Enable logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    # Initialize session variables if they don't exist
    if 'money' not in session:
        session['money'] = 100
    if 'tasks_completed' not in session:
        session['tasks_completed'] = 0
    if 'ceo_name' not in session:
        session['ceo_name'] = "Player"
    if 'cooldown_time' not in session:
        session['cooldown_time'] = 5000  # Initial cooldown time (5 seconds)
    logging.debug(f"Home Route - Session state: {session}")
    return render_template('index.html', ceo_name=session['ceo_name'], money=session['money'], tasks_completed=session['tasks_completed'], cooldown_time=session['cooldown_time'])

@app.route('/set_name', methods=['POST'])
def set_name():
    session['ceo_name'] = request.form['player_name']
    logging.debug(f"Player name set to: {session['ceo_name']}")
    return redirect('/')

@app.route('/upgrades')
def upgrades():
    logging.debug(f"Upgrades Route - Session state: {session}")
    return render_template('upgrades.html')  # Render the upgrades page

@app.route('/write_code', methods=['POST'])
def write_code():
    try:
        logging.debug(f"Before writing code - Session state: {session}")
        session['money'] += 50  # Base money earned per task
        session['tasks_completed'] += 1
        logging.debug(f"After writing code - Session state: {session}")
        return jsonify({
            'ceo_name': session['ceo_name'], 
            'money': session['money'], 
            'tasks_completed': session['tasks_completed'],
            'cooldown_time': session['cooldown_time']
        })
    except Exception as e:
        logging.error(f"Error in write_code: {e}")
        return jsonify({'error': 'Something went wrong during write_code'}), 500

@app.route('/purchase_upgrade', methods=['POST'])
def purchase_upgrade():
    upgrade = request.json
    try:
        logging.debug(f"Upgrade Request: {upgrade}")
        
        if upgrade['effect'] == 'money' and session['money'] >= upgrade['cost']:
            session['money'] -= upgrade['cost']  # Deduct the cost of the upgrade
            session['tasks_completed'] += upgrade['value']  # Increase tasks completed for money-based upgrades
            logging.debug(f"Money upgrade applied. New money: {session['money']}")
            return jsonify({
                'ceo_name': session['ceo_name'], 
                'money': session['money'], 
                'tasks_completed': session['tasks_completed'],
                'message': f"Upgrade purchased! {upgrade['effect']} increased.",
                'cooldown_time': session['cooldown_time']
            })
        
        elif upgrade['effect'] == 'cooldown' and session['money'] >= upgrade['cost']:
            session['money'] -= upgrade['cost']
            session['cooldown_time'] -= upgrade['value'] * 1000  # Decrease the cooldown time
            logging.debug(f"Cooldown upgrade applied. New cooldown time: {session['cooldown_time']}")
            return jsonify({
                'ceo_name': session['ceo_name'], 
                'money': session['money'],
                'message': f"Upgrade purchased! {upgrade['effect']} reduced.",
                'cooldown_time': session['cooldown_time']
            })
        else:
            logging.error("Not enough money for this upgrade!")
            return jsonify({'error': 'Not enough money for this upgrade!'}), 400
    except Exception as e:
        logging.error(f"Error in purchase_upgrade: {e}")
        return jsonify({'error': 'Something went wrong during upgrade purchase'}), 500

if __name__ == '__main__':
    app.run(debug=True)
