from models import Schema
from services import CarService, EmployeService, ClientService
from flask import Flask, render_template, redirect, url_for, request, session
from markupsafe import escape

app = Flask(__name__)

'''
this secret key can be used to access
cookie information about the session.
I do not take care of it here, if you
are using this code, please set a really
secret key
'''
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#@app.route('/test')
#def teste():
#    return render_template('car_form.html')

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('car_table'))
    else:
        return redirect(url_for('login', msg='welcome'))

@app.route('/login/<msg>')
def login(msg):
    if 'username' not in session:
        return render_template('login.html', msg=msg)
    return redirect('/')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('login', msg='welcome'))
    return redirect(url_for('index'))

@app.route('/send', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        if EmployeService().get_access(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect('/')
        return redirect(url_for('login', msg='try again or '))
    return redirect(url_for('login', msg='erro at verb, contact your administrator'))

@app.route('/car_table')
def car_table():
    if 'username' in session:
        columns = ['name', 'username', 'plate', 'model', 'color']
        table = CarService().read_car_table(columns)
        return render_template('car_table.html', table=table)
    return redirect(url_for('index'))

@app.route('/add_table_row/<msg>')
def add_table_row(msg):
    if 'username' in session:
        return render_template('add_table_row.html', msg=msg)
    return redirect(url_for('index'))

@app.route('/add_car_row', methods=['GET', 'POST'])
def add_car_row():
    if 'username' in session:
        if request.method == 'POST':
            columns = {
                'is_parked': 1
            }
            conditions = f"plate = '{request.form['plate']}'"
            if CarService().update(columns, conditions):
                return redirect(url_for('car_table'))
            return redirect(url_for('add_table_row', msg="can't find the car in our database"))
        return redirect(url_for('add_table_row', msg="verb need to be POST, please, call your admin"))
    return redirect(url_for('index'))

@app.route('/rm_car_row/<plate>')
def rm_car_row(plate):
    if 'username' in session:
        if request.method == 'GET':
            columns = {
                'is_parked': 0
            }
            conditions = f"plate = '{plate}'"
            CarService().update(columns, conditions)
            return redirect(url_for('car_table'))
        return redirect(url_for('car_table'))
    return redirect(url_for('index'))
    
@app.route('/create_account/<msg>')
def create_account(msg):
    return render_template('employe_form.html', msg=msg)

@app.route('/create_employe', methods=['POST', 'GET'])
def create_employe():
    if request.method == 'POST':
        columns = {
            'name': request.form['name'],
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form['email']
        }
        if EmployeService().create(columns):
            return redirect(url_for('login', msg='welcome'))
        return redirect(url_for('create_account', msg='try again'))
    return redirect(url_for('create_account', msg='erro at verb, contact your administrator or try to connect before'))

@app.route('/new_client/<msg>')
def new_client(msg):
    if 'username' in session:
        return render_template('client_form.html', msg=msg)
    return redirect(url_for('index'))

@app.route('/create_client', methods=['POST', 'GET'])
def create_client():
    if request.method == 'POST':
        if 'username' in session:
            columns = {
                'name': request.form['name'],
                'username': request.form['username'],
                'email': request.form['email']
            }
            if ClientService().create(columns):
                return redirect(url_for('new_client', msg="success"))
            return redirect(url_for('new_client', msg="try again"))
        return redirect(url_for('index'))
    return redirect(url_for('new_client', msg='verb need to be POST, contact your administrator'))
    
@app.route('/new_car/<msg>')
def new_car(msg):
    if 'username' in session:
        return render_template('car_form.html', msg=msg)
    return redirect(url_for('index'))

@app.route('/create_car', methods=['POST', 'GET'])
def create_car():
    if request.method == 'POST' and 'username' in session:
        columns = ['username']
        conditions = "username = '" + request.form['owner'] + "'"
        if ClientService().read(columns, conditions):
            columns = {
                'plate': request.form['plate'],
                'model': request.form['model'],
                'color': request.form['color'],
                'owner': request.form['owner']
            }
            if CarService().create(columns):
                return redirect(url_for('car_table'))
            return redirect(url_for('new_car', msg='try again'))
        return redirect(url_for('new_car', msg='invalid username'))
    return redirect(url_for('new_car', msg='erro at verb, contact your administrator or try to connect before do it'))

if __name__ == '__main__':
    Schema()
    app.run(debug=True)