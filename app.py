from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Initial game data
ceo_name = "Player"
money = 100
tasks_completed = 0
cooldown_time = 5000  # Initial cooldown time (5 seconds)

@app.route('/')
def home():
    return render_template('index.html', ceo_name=ceo_name, money=money, tasks_completed=tasks_completed)

@app.route('/set_name', methods=['POST'])
def set_name():
    global ceo_name
    ceo_name = request.form['player_name']
    return redirect('/')

@app.route('/upgrades')
def upgrades():
    return render_template('upgrades.html')  # Render the upgrades page

@app.route('/write_code', methods=['POST'])
def write_code():
    global money, tasks_completed
    try:
        money += 50  # Base money earned per task
        tasks_completed += 1
        # Respond with the updated data as JSON
        return jsonify({
            'ceo_name': ceo_name, 
            'money': money, 
            'tasks_completed': tasks_completed
        })
    except Exception as e:
        print(f"Error in write_code: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@app.route('/solve_ticket', methods=['POST'])
def solve_ticket():
    global money, tasks_completed
    try:
        money += 30  # Base money earned per solved ticket
        tasks_completed += 1
        # Respond with the updated data as JSON
        return jsonify({
            'ceo_name': ceo_name, 
            'money': money, 
            'tasks_completed': tasks_completed
        })
    except Exception as e:
        print(f"Error in solve_ticket: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)
