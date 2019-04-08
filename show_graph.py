from flask import Flask,jsonify, request, render_template
from creategraph import send_data_table,send_graph

app = Flask(__name__)
@app.route('/')
def db():
    return render_template("smart_irrig.html")

@app.route('/show1', methods=['GET','POST'])
def getvalue():
    data = send_graph()
    return jsonify( data)

@app.route('/show2',methods=['GET','POST'])
def gettable():
    data = send_data_table()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
