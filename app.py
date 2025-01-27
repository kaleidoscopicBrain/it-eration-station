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
        # Respond with the updated data as JSON
        return jsonify({
            'ceo_name': session['ceo_name'], 
            'money': session['money'], 
            'tasks_completed': session['tasks_completed']
        })
    except Exception as e:
        print(f"Error in write_code: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@app.route('/solve_ticket', methods=['POST'])
def solve_ticket():
    try:
        session['money'] += 30  # Base money earned per solved ticket
        session['tasks_completed'] += 1
        # Respond with the updated data as JSON
        return jsonify({
            'ceo_name': session['ceo_name'], 
            'money': session['money'], 
            'tasks_completed': session['tasks_completed']
        })
    except Exception as e:
        print(f"Error in solve_ticket: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@app.route('/purchase_upgrade', methods=['POST'])
def purchase_upgrade():
    upgrade = request.json
    if upgrade['effect'] == 'money' and session['money'] >= upgrade['cost']:
        session['money'] -= upgrade['cost']
        session['tasks_completed'] += upgrade['value']
        return jsonify({
            'ceo_name': session['ceo_name'], 
            'money': session['money'], 
            'tasks_completed': session['tasks_completed'],
            'message': f"Upgrade purchased! {upgrade['effect']} increased."
        })
    elif upgrade['effect'] == 'cooldown' and session['money'] >= upgrade['cost']:
        session['money'] -= upgrade['cost']
        session['cooldown_time'] -= upgrade['value'] * 1000
        return jsonify({
            'ceo_name': session['ceo_name'], 
            'money': session['money'],
            'message': f"Upgrade purchased! {upgrade['effect']} reduced."
        })
    else:
        return jsonify({'error': 'Not enough money for this upgrade!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
