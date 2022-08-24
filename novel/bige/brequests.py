import requests
import re
from lxml import etree

def book_requests(url):
    try:
        response = requests.get(url)
        encoding = re.findall('<meta.*?charset="?([\w-]*).*>', response.text, re.I)[0]
        response.encoding = encoding
        return etree.HTML(response.text)
    except requests.exceptions.RequestException as e:
        print(e)