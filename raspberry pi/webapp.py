from flask import Flask, render_template, request, session, g, url_for, redirect
from sense_emu import SenseHat
import random
s=SenseHat() 
green = [0,200,0]
black = [0,0,0]
shipmap = [green]*10 + [black]*54
app = Flask(__name__)

app.secret_key = "paok"

users = []
users.append([1, 'd', 'd'])
users.append([2, 'Maria', 'kodikos_Marias'])

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        for user in users:
            if user[0] == session['user_id']:
                g.user=user
                g.s = s
                

@app.route('/')
def index():
    
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('index.html')

@app.route('/logme', methods=['POST', 'GET'])
def logme():
    session.pop('user_id', None)
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        for user in users:
            if user[1] == username and user[2] == password:
                session['user_id'] = user[0]
                return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/sense')
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('senses.html')

@app.route('/ships', methods=['POST','GET'])
def naymaxia():
    s.clear()
    if not g.user:
        return redirect(url_for('logme'))
    if request.method == 'POST':
        katheta = int(request.form['kath'])
        orizontia = int(request.form['oriz'])
        s.set_pixel(orizontia,katheta,[0,0,255])
        if katheta > 7 :
            random.shuffle(shipmap)
            s.set_pixels(shipmap)
    return render_template('ships.html')

@app.context_processor
def a_processor(): 
    def roundv(value,digits):
        return round(value,digits)
    return {'roundv':roundv}



if __name__ == '__main__':
    app.run(debug=True)
