import os
import io
import sys
import string
import traceback
import jsonpickle
import random
from datetime import datetime, timezone, timedelta
from flask import Flask, g,request, json, send_file, abort, Response
from flask import render_template, redirect, url_for, flash, jsonify,send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES,UploadNotAllowed

""" Framework init boilerplate"""
def thisdir():
    return os.path.dirname(os.path.abspath(__file__))
def add_to_path(directory):
    if directory not in sys.path:
        sys.path.append(directory)
conf_dir=thisdir()
while not os.path.exists(os.path.join(conf_dir,"app_config.py")):
    conf_dir = os.path.dirname(conf_dir)
    if len(conf_dir)<2:
        print("Unable to find config")
        sys.exit()
add_to_path(conf_dir)
from app_config import settings
if "pythondirs" in settings:
    for d in settings["pythondirs"]:
        add_to_path(os.path.join(conf_dir,*d))
""" Framework boilerplate done"""
        
is_site_down = False
debug=True
try:
    """
    SITE-SPECIFIC IMPORTS
    """
except Exception as e:
    import traceback
    print("{0} Import Error: {1}".format(__file__,e))
    print(traceback.format_exc())
    print("path:{0}".format("\n".join(sys.path)))
    is_site_down = True
    
app = Flask(__name__, template_folder=os.path.join(thisdir(), 'templates'))

SECRET_KEY = "SECRET_KEY"
DEBUG = False
app.config.from_object(__name__)


LOGO = """/static/images/logo.png"""

SOCIAL=[
"twitter",
"facebook",
"youtube",
"instagram"
]
BANNER=[
"""/static/images/banner1.jpg""",
"""/static/images/banner2.jpg""",
"""/static/images/banner3.jpg"""
]
FOOTER=[
""



]
CONTACTS=[
"""Tel: <a href="tel:+08000000000">0800 0000 000</a><br>""",
"""WhatsApp: <a href="tel:+08000000000">0800 0000 000</a><br>""",
"""Email: <a href="mailto:info@securemybin.com">info@securemybin.com</a><br>""",
]
COPYRIGHT=[
"""Copyright &copy; 2020 Demo<br>
Registered in Everywhere | Registered address as contact address<br>
Website Design by <a href="#" rel="nofollow" target="_blank">Us</a>
"""
]

CARDS = [
{
"image_path": "/static/images/new-years-eve-1911483__340.webp",
"image_alt" : "image",
"card_title" : "SUPER CARD",
"card_text" : "this is the text for this card",
"button_link" : "#",
"button_text" : "LEARN MORE"
},
{
"image_path": "/static/images/sunset-1645105__340.webp",
"image_alt" : "image2",
"card_title" : "SUPER CARD 2",
"card_text" : "this is the text for this cardddd",
"button_link" : "#",
"button_text" : "LEARN MORE 2"
}
]

TIMELINE = [
    "timeline title",
    [
        {
            "title": "WEB DESIGN",
            "date" : "21 March, 2009",
            "text" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque scelerisque diam non nisi semper"
                     ", et elementum lorem ornare. Maecenas placerat facilisis mollis."
        },
        {
            "title": "GRAPHIC DESIGN",
            "date" : "21 April, 2003",
            "text" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque scelerisque diam non nisi semper"
                     ", et elementum lorem ornare. Maecenas placerat facilisis mollis."
        },
        {
            "title": "HTML/CSS",
            "date" : "23 May, 2000",
            "text" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque scelerisque diam non nisi semper"
                     ", et elementum lorem ornare. Maecenas placerat facilisis mollis."
        }
    ]
]

PROGRESS_BARS = [
    {
        "name" : "HTML",
        "value" : "50"
    },
    {
        "name" : "PHP",
        "value" : "70"
    },
    {
        "name" : "CSS",
        "value" : "90"
    }
]

MENU_ITEMS ={
    "about":{
        "template" : "about.html",
        "name" : "About",
        "vars":{
            "columns":1,
            "tworows":True,
            "secondrowcols":2
        }
        
    },
    "why":{
        "template" : "why.html",
        "name" : "Why Lock?",
        "vars":{
            "tworows":True,
            "secondrowcols":2
        }
    },
    "buy":{
        "template" : "buy.html",
        "name" : "Buy Locks & Accessories",
        "vars":{
            "tworows":True,
            "secondrowcols":1
        }
    },
    "book":{
        "template" : "book.html",
        "name" : "Book an Installation",
        "vars":{
            "tworows":True,
            "secondrowcols":1
        }
    },
    "news":{
        "template" : "news.html",
        "name" : "News"
    }
}



#Defaults for the entire site
site_vars = {
        "columns":1, #no of cols for the 1st main content row
        "tworows":False, #if true, the 2n row for content is builded
        "boxed":True,  #True for boxed, False for full width
        "footer_columns" :3,
        "logo":LOGO, #path to logo
        "social": SOCIAL, #social icons.
        "banner": BANNER, #paths to slider images
        "contacts": CONTACTS,
        "copyright": COPYRIGHT[0],
        "menuitems":MENU_ITEMS
}

ADDRESSES=[
    ["11 Some Street","12 Some Street","13 Some Street","14 Some Street"],
    ["101 Some Street","102 Some Street","103 Some Street","104 Some Street"],
    ["131 Some Street","132 Some Street","133 Some Street","134 Some Street"],
    ["121 Some Street","122 Some Street","123 Some Street","124 Some Street"]
]

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']


        
@app.before_request
def check_for_site_down():
    if is_site_down and request.path != url_for('site_down'):
        return redirect(url_for('site_down'))

@app.route('/site_down')
def site_down():
    if is_site_down:
        return 'Sorry, site_down!', 503
    else:
        return redirect("/")

def render_path(subpath=None):
    conf_vars=site_vars
    template=MENU_ITEMS.get(subpath,{}).get('template',"index.html")
    page_vars=MENU_ITEMS.get(subpath,{}).get('vars',{})
    conf_vars.update(page_vars)        
    return render_template(template,vars=conf_vars)


@app.route("/", methods=["GET"])
def index():
    return render_path()

@app.route("/<path:subpath>", methods=["GET"])
def path(subpath):
    return render_path(subpath)


# JSON parameters
# postcode
def address_lookup(jsondata):
    if 'postcode' in jsondata:
        return random.choice(ADDRESSES)

# JSON parameters
# address
# postcode
# date
def next_available(jsondata):
    if 'address' in jsondata:
        date=datetime.fromisoformat(jsondata.get('date'))
        days = []
        for i in range(5):
            days.append(date+timedelta(days=random.choice(range(12))))
        return {'slots': days}

# JSON parameters
# address
# postcode
# date
def list_slots(jsondata):
    if 'address' in jsondata:
        date=datetime.fromisoformat(jsondata.get('date'))
        hours = []
        for j in range(3):
            hours.append(date+timedelta(hours=random.choice(range(8, 20))))
        return {'hours': sorted(hours)}

def test(jsondata):
    return "ok"

handlers={}
handlers["address_lookup"]=address_lookup
handlers["next_available"]=next_available
handlers["list_slots"]=list_slots
handlers["test"]=test

def handle_api(req_type,jsondata):
    resp={"error":"Invalid Request"}
    try:
        resp=handlers[req_type](jsondata)
    except Exception as e:
        resp={"error":"{}".format(e)}
    return Response(jsonpickle.encode(resp,False), mimetype='application/json')                    

   


@app.route("/api/<path:req_type>", methods=["POST"])
def apicall(req_type):
    return handle_api(req_type,request.json)
    
