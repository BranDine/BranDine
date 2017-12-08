"""
    BranDine
	Developers:

	To run this you need to execute the following shell commands
	% pip3 install flask
	% pip3 install flash_oauthlib
	% python3 mktypapp.py

	For windows just don't type the "3"s

    The authentication comes from an app by Bruno Rocha
    GitHub: https://github.com/rochacbruno
"""
from functools import wraps
from flask import Flask, redirect, url_for, session, request, jsonify, render_template, request
from flask_oauthlib.client import OAuth
from datetime import datetime

app = Flask(__name__)
#gracehopper.cs-i.brandeis.edu:5000
#app.config['GOOGLE_ID'] = '783502545148-f4a0ss6kdf839iekmreq1inl2lqnhaqt.apps.googleusercontent.com'
#app.config['GOOGLE_SECRET'] = '9WksdPKQfOG77hO3DDteRFYr'

#127.0.0.1:5000
app.config['GOOGLE_ID'] = '246096591118-ti33uv184e4m1bib9grgn8alm45btadb.apps.googleusercontent.com'
app.config['GOOGLE_SECRET'] = 'iqgLqu6pXgLuHsZFq6nvxDX3'

app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not('google_token' in session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/main')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        print("logged in")
        print(jsonify(me.data))
        return render_template("main.html")
        #return jsonify({"data": me.data})
    print('redirecting')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    #
    return redirect(url_for('main'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    print(session['google_token'])
    me = google.get('userinfo')
    session['userinfo'] = me.data
    print(me.data)
    return render_template("main.html")
    #return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')



@app.route('/')
def main():
	return render_template("main.html")

@app.route('/team')
def team():
	return render_template('team.html')

@app.route('/testing')
def testing():
	return render_template('testing.html')

@app.route('/arlene')
def arlene():
	return render_template('arlene.html')

@app.route('/stephanie')
def stephanie():
	return render_template('stephanie.html')

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
	global reviews
	print('in reviews')
	for review in reviews:
		print(review)
	return render_template('reviews.html',reviews=reviews)

@app.route('/writeReview')
def writeReview():
	return render_template('writeReview.html')

reviews=[]
reviewCounter=0

@app.route('/processReview',methods=['GET','POST'])
def processReview():
	global reviews
	global reviewCounter
	print("in processReview")
	print(reviews)
	if request.method == 'POST':
		userinfo = session['userinfo']
		who = userinfo['email']
		location = request.form['location']
		lines = request.form['lines']
		review = request.form['review']
		now = datetime.now()
		print(reviewCounter)

		review = {
            'id':reviewCounter,
            'location':location,
            'time':now,
            'lines':lines,
            'who':who,
            'review':review
            }
		print(review)
		reviewCounter = reviewCounter + 1
		reviews.insert(0,review) # add msg to the front of the list
		print('sending reviews to reviews.htmls')
		print(reviews)
		sortedReviews = sorted(reviews, key=lambda k: k['location'])
	return render_template("reviews.html",reviews=sortedReviews)

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)
