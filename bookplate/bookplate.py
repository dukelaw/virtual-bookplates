"""Bookplate app

###app.config.from_envar('FLASKR_SETTINGS', silent=True)

###request.form['doc_number']
###http://localhost:8050/005031541

### to activate environment = . env/bin/activate

"""
from flask import Flask, render_template, redirect, url_for
import urllib
import requests
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e, message=None):
    return render_template('404.html', message=message), 404

@app.route('/<hol_number>') ### get doc_number
def get_hol(hol_number):

    if re.match("\d{1,9}$", hol_number) is None:
        message = "This holding number is not valid" # check for valid holding record numbers
        return page_not_found(404, message=message)
    elif re.match("\d{1,8}$", hol_number):
        return redirect(hol_number.zfill(9))
    url = "http://catalog.library.duke.edu/X?&base=duk60&doc_number=" + hol_number + "&op=find-doc"
    r = requests.get(url)
    text = r.text
    root = ET.fromstring(text) ### creates XML element

    bookplate_list = []
    bookplate_text_a = root.findtext('.//varfield[@id="541"]/subfield[@label="a"]')
    bookplate_text_c = root.findtext('.//varfield[@id="541"]/subfield[@label="c"]')
    bookplate_text = bookplate_text_a + bookplate_text_c

    if bookplate_text is not None: ### check for plate
        bookplate_list = bookplate_text.split(';')
    else:
        message = "This book doesn't have an award plate" # check for an actual award plate
        return page_not_found(404, message=message)

    bookplate_date = root.findtext('.//varfield[@id="541"]/subfield[@label="d"]')

    if bookplate_date is not None:
        bookplate_list.append(bookplate_date)

    bib_number = root.findtext('.//varfield[@id="LKR"]/subfield[@label="b"]')
    result = "\n".join(bookplate_list)
    return render_template('index.html', bookplate_list=bookplate_list, hol_number=hol_number, bookplate_date=bookplate_date, bib_number=bib_number)
