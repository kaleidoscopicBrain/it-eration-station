from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Initial game data
ceo_name = "Player"
money = 100
tasks_completed = 0

@app.route('/')
def home():
    return render_template('index.html', ceo_name=ceo_name, money=money, tasks_completed=tasks_completed)

@app.route('/set_name', methods=['POST'])
def set_name():
    global ceo_name
    ceo_name = request.form['player_name']
    return redirect('/')

@app.route('/write_code', methods=['POST'])
def write_code():
    global money, tasks_completed
    try:
        money += 50
        tasks_completed += 1
        
        # Return updated data as JSON for AJAX
        if request.is_xhr or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'money': money, 'tasks_completed': tasks_completed})
        
    except Exception as e:
        print("Error in write_code:", e)  # Log the error
        return jsonify({'error': 'Something went wrong in write_code'}), 500

    return redirect(url_for('home'))

@app.route('/solve_ticket', methods=['POST'])
def solve_ticket():
    global money, tasks_completed
    try:
        money += 30
        tasks_completed += 1
        
        # Return updated data as JSON for AJAX
        if request.is_xhr or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'money': money, 'tasks_completed': tasks_completed})
        
    except Exception as e:
        print("Error in solve_ticket:", e)  # Log the error
        return jsonify({'error': 'Something went wrong in solve_ticket'}), 500

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
