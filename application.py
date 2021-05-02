from flask import Flask, render_template, request
import requests
import pandas as pd
import datetime
import json

application = Flask(__name__)

@application.route('/')
@application.route('/index.html')
def index():
    return render_template('index.html')

@application.route('/about.html')
def about():
    return render_template('about.html')

@application.route('/dates.html' ,methods=['POST'])
def getDates():
    try:
        pincode  = request.form['pincode']
        date = request.form['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%y')
        #print(date)
        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(pincode)+"&date="+date)
        #print('respone',response.text)
        #print(response.text)

        s = json.loads(response.text)
        #print(s.keys())
        if 'error' in s.keys():
            if s['error'] == 'Invalid Pincode':
                return render_template('dates.html', rows = [],invalid="invalid",pincode = "pincode",date = date)
            #print(s['sessions'])
        else:
            df = pd.DataFrame(s['sessions'])
            rows = []
            for i,r in df.iterrows():
                #r.pop('slots')
                r['CenterName'] = r['name']
                #print(r)
                rows.append(r)
    except:
        print('something went wrong.')

    #print(rows)
    return render_template('dates.html', rows = rows,pincode = pincode,date = date)

if __name__ == '__main__':
    application.run()
