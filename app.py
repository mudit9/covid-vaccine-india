from flask import Flask, render_template, request
import requests
import pandas as pd
import datetime
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/dates.html' ,methods=['POST'])
def getDates():
    pincode  = request.form['pincode']
    date = request.form['date']
    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%y')
    print(date)
    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(pincode)+"&date="+date)
    #print('respone',response.text)
    s = json.loads(response.text)
    #print(s['sessions'])
    df = pd.DataFrame(s['sessions'])
    rows = []
    for i,r in df.iterrows():
        #r.pop('slots')
        r['CenterName'] = r['name']
        print(r)
        rows.append(r)

    #print(rows)
    return render_template('dates.html', rows = rows,pincode = pincode,date = date)

if __name__ == '__main__':
    #app.run(debug=True)
    #print(datetime.__version__)
    print(requests.__version__)
    print(json.__version__)
    print(pd.__version__)
