import collections
from re import M
from time import sleep
from json2html import * 
import requests, psycopg2, json
from flask import Flask, render_template, request



url = "https://solana-gateway.moralis.io/nft/mainnet/{}/metadata"
headers = {
    "accept": "application/json",
    "X-API-Key": "WBgAeLB5DJxduGfcgTMlc4XmW9PVa3kCstYJF1e170NmNIYEbxWYNytr2oxtvd1i"
}



conn = psycopg2.connect(database="nft", user = "postgres", password = "qwerty123", host = "localhost", port = "5432")
cur = conn.cursor()


cur.execute('CREATE TABLE IF NOT EXISTS nft(address TEXT PRIMARY KEY, discription VARCHAR(1000))')
conn.commit()

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def search():
    if request.method=='POST':
        address=request.form.get('address')
        response=requests.get(url.format(address), headers=headers).json()
        cur=conn.cursor()
        res=str(response)
        db1 = bool(cur.rowcount)
        db2 = False
        if db1:
            cur.execute('SELECT discription FROM nft WHERE address=%s ',(address,))
            db2 = (cur.fetchone() is not None)   
        if db2:
            cur.execute('SELECT discription FROM nft WHERE address=%s ',(address,))
            rows=cur.fetchall
        else:    
            cur.execute('INSERT INTO nft(address, discription) VALUES (%s,%s);',(address,res))
            conn.commit()
        
        
            

        return render_template('output.html', out = response)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)