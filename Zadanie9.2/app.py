import requests
from flask import Flask, render_template, request
import csv

app = Flask(__name__)
response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = []
for item in data:
    for data_item in item['rates']:
        rates.append(data_item)
keys = rates[0].keys()

a_file = open("my_csv.csv", "w")
dict_writer = csv.DictWriter(a_file, keys, delimiter=";")
dict_writer.writeheader()
dict_writer.writerows(rates)
a_file.close()

@app.route('/formularz', methods=['GET' , 'POST'])
def formularz():
    return render_template("formularz.html")





if __name__ == '__main__':
    app.run(debug=True)
