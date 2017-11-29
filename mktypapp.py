from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def main():
	return render_template("main.html")

@app.route('/team')
def team():
	return render_template('team.html')

@app.route('/momina')
def momina():
	return render_template('momina.html')

@app.route('/pitch')
def pitch():
	return render_template('pitch.html')

@app.route('/formdemo')
def formdemo():
	return render_template('formdemo.html')

@app.route('/menu')
def menu():
	return render_template('menu.html')


@app.route('/style.css')
def css():
	return render_template('style.css')


@app.route('/feed')
def feed():
	return render_template('feed.html')

@app.route('/traffic')
def traffic():
	return render_template('traffic.html')

@app.route('/reviews')
def reviews():
	return render_template('reviews.html')
 
if __name__ == '__main__':
    app.run('0.0.0.0',port=3000)
