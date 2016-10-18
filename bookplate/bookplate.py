from flask import Flask, render_template
import urllib
import requests
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)


###app.config.from_envar('FLASKR_SETTINGS', silent=True)

###request.form['doc_number']
###http://localhost:8050/005031541

### to activate environment = . env/bin/activate



@app.route('/<hol_number>') ### get doc_number
def get_hol(hol_number):
    if re.match("\d{9}", hol_number) is None:

        return None

    url = "http://catalog.library.duke.edu/X?&base=duk60&doc_number=" + hol_number + "&op=find-doc"
    r = requests.get(url)
    text = r.text
    root = ET.fromstring(text) ### creates XML element


    bookplate_list = []
    bookplate_text = root.findtext('.//varfield[@id="541"]/subfield[@label="c"]')
    print(bookplate_text)
    if bookplate_text is not None:
        bookplate_list = bookplate_text.split(';')

    bookplate_date = root.findtext('.//varfield[@id="541"]/subfield[@label="d"]')

    bookplate_list.append(bookplate_date)
    bib_number = root.findtext('.//varfield[@id="LKR"]/subfield[@label="b"]')
    print(bib_number)
    print("Here is the bookplate list:")
    print(bookplate_list)
    result = "\n".join(bookplate_list)
    print("This is the result:")
    print(result)




    return render_template('index.html', bookplate_list=bookplate_list, hol_number=hol_number, bookplate_date=bookplate_date, bib_number=bib_number)

# def remove_space

### get.request on URL to generate HTML





##class_year = r.text['541']['d']
