import os
import sys

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'flaskengine'))


from flask import Flask
from flaskengine import flaskengine_bp


app = Flask(__name__)
app.config.update(
    FE_TITLE='Flask Engine Example',
    FE_NAV_BAR={'Example': 'greeting.greeting_list'},
    FE_LAND_URL='/'
)
#Register The Blueprint to use the templates and static files
app.register_blueprint(flaskengine_bp)

from google.appengine.ext import ndb


class Greeting(ndb.Model):
    author = ndb.StringProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


# Lets generate some view's
from flaskengine import IndexView, ModelList, ModelDelete, ModelEdit, ModelCreate
from flask import Blueprint


greeting_bp = Blueprint('greeting', __name__)


# Generate a index view that will extend the base template.
class ExampleIndex(IndexView):
    endpoint = '/'
    index_template = 'welcome.html'
    admin = False


# List view for given model that will be rendered in table.
class GreetingList(ModelList):
    admin = False
    model = Greeting
    display_values = ['author', 'content', 'date']
    display_order = 'date'


#Delete view for a model entity
class GreetingDelete(ModelDelete):
    admin = False
    model = Greeting


#Edit view for a model entity
class GreetingEdit(ModelEdit):
    admin = False
    model = Greeting


#Create view for a model entity
class GreetingCreate(ModelCreate):
    admin = False
    model = Greeting


#Register All views with Blueprint
ExampleIndex.register_bp(greeting_bp)
GreetingList.register_bp(greeting_bp)
GreetingDelete.register_bp(greeting_bp)
GreetingEdit.register_bp(greeting_bp)
GreetingCreate.register_bp(greeting_bp)


#Register Blueprint with the app
app.register_blueprint(greeting_bp, url_prefix='')
