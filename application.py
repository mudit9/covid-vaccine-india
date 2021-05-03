from flask import Flask, render_template, request
import requests
import pandas as pd
from datetime import date, timedelta, datetime

import json

application = Flask(__name__)

@application.route('/')
@application.route('/index.html')
def index():
    return render_template('index.html')

@application.route('/about.html')
def about():
    return render_template('about.html')

@application.route('/multiplenextdates')
def getSlotsMultipleNextDay():
    try:
         #pincode = request.args.get('pincode')
         date = request.args.get('date')
         #vars = request.args.get('vars')
         pincodes = request.args.getlist('pincodes')
         pincodes = pincodes[0].replace("'", "").replace('[',"").replace(']',"")
         pincodes = pincodes.split(',')
         print(pincodes,len(pincodes))

         date_time_obj = datetime.strptime(date, '%d/%m/%y')
         tomorrow = date_time_obj + timedelta(days = 1)
         date = datetime.strptime(str(tomorrow), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y')
         multirows = []
         invalids = []
         for pincode_item in pincodes:
             print(str(pincode_item))
             response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(pincode_item).strip()+"&date="+date)
             #print('respone',response.text)
             print(response.text)

             s = json.loads(response.text)
             #print(s.keys())
             if 'error' in s.keys():
                 if s['error'] == 'Invalid Pincode':
                     multirows.append([])
                     invalids.append("Invalid Pincode")
                     #return render_template('dates.html', rows = [],invalid="Invalid Pincode",pincode = pincode,date = date)
                 #print(s['sessions'])
             else:
                 df = pd.DataFrame(s['sessions'])
                 print(df.columns)
                 try:
                     df = df.sort_values(by=['min_age_limit'])
                 except Exception as e:
                     print("no min age limit")
                 rows = []
                 for i,r in df.iterrows():
                     Slots = ','.join(r['slots'])

                     r['CenterName'] = r['name']
                     r['Slots'] = Slots
                     #print(r)
                     rows.append(r)
                 invalids.append(None)
                 multirows.append(rows)
         vars = zip(multirows,invalids,pincodes)
         print("invalids",invalids)
         return render_template('multipledates.html',vars = vars,pincodes=pincodes,date = date)
    except Exception as e:
        print(e)
        return render_template('multipledates.html', rows = [],invalid="Something went wrong.",pincode = pincode,date = date)


@application.route('/nextdates')
def getSlotsNextDay():
    try:
         pincode = request.args.get('pincode')
         date = request.args.get('date')
         date_time_obj = datetime.strptime(date, '%d/%m/%y')
         tomorrow = date_time_obj + timedelta(days = 1)
         date = datetime.strptime(str(tomorrow), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y')

         #date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%y')
         response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(pincode)+"&date="+str(date))
         #print('respone',response.text)
         #print(response.text)

         s = json.loads(response.text)
         #print(s.keys())
         if 'error' in s.keys():
             if s['error'] == 'Invalid Pincode':
                 return render_template('dates.html', rows = [],invalid="Invalid Pincode",pincode = "pincode",date = date)
             #print(s['sessions'])
         else:
             df = pd.DataFrame(s['sessions'])
             try:
                 df = df.sort_values(by=['min_age_limit'])
             except Exception as e:
                 print("no min age limit")
             rows = []
             for i,r in df.iterrows():
                 Slots = ','.join(r['slots'])

                 r['CenterName'] = r['name']
                 r['Slots'] = Slots
                 #print(r)
                 rows.append(r)
    except Exception as e:
        print(e)
        return render_template('dates.html', rows = [],invalid="Something went wrong.",pincode = pincode,date = date)
        #print('something went wrong.')

        #print(rows)
    return render_template('dates.html', rows = rows,pincode = pincode,date = date)

@application.route('/dates.html' ,methods=['POST'])
def getDates():
    try:
        pincode  = request.form['pincode']
        date = request.form['date']
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%y')
        #print(date)
        pincodes = pincode.split(',')
        if len(pincodes)>1:
                multirows = []
                invalids = []
                for pincode_item in pincodes:
                    print(str(pincode_item))
                    response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(pincode_item)+"&date="+date)
                    #print('respone',response.text)
                    print(response.text)

                    s = json.loads(response.text)
                    #print(s.keys())
                    if 'error' in s.keys():
                        if s['error'] == 'Invalid Pincode':
                            multirows.append([])
                            invalids.append("Invalid Pincode")
                            #return render_template('dates.html', rows = [],invalid="Invalid Pincode",pincode = pincode,date = date)
                        #print(s['sessions'])
                    else:
                        df = pd.DataFrame(s['sessions'])
                        print(df.columns)
                        try:
                            df = df.sort_values(by=['min_age_limit'])
                        except Exception as e:
                            print("no min age limit")
                        rows = []
                        for i,r in df.iterrows():
                            Slots = ','.join(r['slots'])

                            r['CenterName'] = r['name']
                            r['Slots'] = Slots
                            #print(r)
                            rows.append(r)
                        invalids.append(None)
                        multirows.append(rows)
                vars = zip(multirows, invalids,pincodes)
                print("invalids",invalids)
                return render_template('multipledates.html',vars = vars,pincodes = pincodes,date = date)



        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(pincode)+"&date="+date)
        #print('respone',response.text)
        #print(response.text)

        s = json.loads(response.text)
        #print(s.keys())
        if 'error' in s.keys():
            if s['error'] == 'Invalid Pincode':
                return render_template('dates.html', rows = [],invalid="Invalid Pincode",pincode = pincode,date = date)
            #print(s['sessions'])
        else:
            df = pd.DataFrame(s['sessions'])
            try:
                df = df.sort_values(by=['min_age_limit'])
            except Exception as e:
                print("no min age limit")
            rows = []
            for i,r in df.iterrows():
                Slots = ','.join(r['slots'])

                r['CenterName'] = r['name']
                r['Slots'] = Slots
                #print(r)
                rows.append(r)
    except Exception as e:
        print(e)
        return render_template('dates.html', rows = [],invalid="Something went wrong.",pincode = pincode,date = date)

    #print(rows)
    return render_template('dates.html', rows = rows,pincode = pincode,date = date)

if __name__ == '__main__':
    application.run(debug=True)
