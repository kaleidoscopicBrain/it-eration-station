from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Initial game data
ceo_name = "Player"
money = 100
tasks_completed = 0

@app.route('/')
def home():
    return render_template('index.html', ceo_name=ceo_name, money=money, tasks_completed=tasks_completed)

@app.route('/write_code', methods=['POST'])
def write_code():
    global money, tasks_completed
    money += 50
    tasks_completed += 1
    return redirect(url_for('home'))

@app.route('/solve_ticket', methods=['POST'])
def solve_ticket():
    global money, tasks_completed
    money += 30
    tasks_completed += 1
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
