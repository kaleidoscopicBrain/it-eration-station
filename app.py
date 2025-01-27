from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)

# Set a secret key for session management (This should be kept secret in a real application)
app.secret_key = 'your_secret_key_here'

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
    return render_template('index.html', ceo_name=session['ceo_name'], money=session['money'], tasks_completed=session['tasks_completed'])

@app.route('/set_name', methods=['POST'])
def set_name():
    session['ceo_name'] = request.form['player_name']
    return redirect('/')

@app.route('/upgrades')
def upgrades():
    return render_template('upgrades.html')  # Render the upgrades page

@app.route('/write_code', methods=['POST'])
def write_code():
    try:
        session['money'] += 50  # Base money earned per task
        session['tasks_completed'] += 1
        return jsonify({
            'ceo_name': session['ceo_name'], 
            'money': session['money'], 
            'tasks_completed': session['tasks_completed'],
            'cooldown_time': session['cooldown_time']
        })
    except Exception as e:
        print(f"Error in write_code: {e}")
        return jsonify({'error': 'Something went wrong during write_code'}), 500

@app.route('/purchase_upgrade', methods=['POST'])
def purchase_upgrade():
    upgrade = request.json
    try:
        if upgrade['effect'] == 'money' and session['money'] >= upgrade['cost']:
            session['money'] -= upgrade['cost']  # Deduct the cost of the upgrade
            session['tasks_completed'] += upgrade['value']  # Increase tasks completed for money-based upgrades
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
            return jsonify({
                'ceo_name': session['ceo_name'], 
                'money': session['money'],
                'message': f"Upgrade purchased! {upgrade['effect']} reduced.",
                'cooldown_time': session['cooldown_time']
            })
        else:
            return jsonify({'error': 'Not enough money for this upgrade!'}), 400
    except Exception as e:
        print(f"Error in purchase_upgrade: {e}")
        return jsonify({'error': 'Something went wrong during upgrade purchase'}), 500

if __name__ == '__main__':
    app.run(debug=True)
