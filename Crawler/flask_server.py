from flask import Flask,jsonify,request,render_template
import sqlite3

app = Flask(__name__)



#post /store data: {name :}
@app.route('/word_count' , methods=['POST'])
def create_store():
    request_data = request.get_json()
    conn = sqlite3.connect('data/WordCount.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS WordCountTable (
            Date TEXT NOT NULL,
            Company TEXT NOT NULL,
            WordCount INT NOT NULL,
            PRIMARY KEY (Date, Company)
            );''')
    l = [request_data['Date'], request_data['Company'], request_data['Count']]
    #l = list(dict1.values())
    cursor = conn.execute("SELECT WordCount FROM WordCountTable where Date = \"" + str(l[0]) + "\" and Company = \"" + str(l[1]) + "\";")
    has_instance = 0
    WordCount = 0
    for row in cursor:
        WordCount += row[0]
        has_instance = 1
    if(not has_instance):
        conn.execute("INSERT INTO WordCountTable VALUES (\"" + str(l[0]) + "\", \"" + str(l[1]) + "\"," + str(l[2]) + ")")
    else:
        WordCount += l[2]
        conn.execute("UPDATE WordCountTable SET WordCount = \"" + str(WordCount) + "\" where Date = \"" + str(l[0]) + "\" and Company = \"" + str(l[1]) + "\";")
    conn.commit()
    conn.close()
    new_store = {
        'name': 'fwfewfwf',
        'items':[]
    }
    return jsonify(new_store)


app.run(port=5000)