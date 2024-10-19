from flask.blueprint import Blueprint
from App.user import user_views
from App.index import index_views
from App.auth import auth_views
from App.admin import setup_admin


views: list[Blueprint] = [user_views, index_views, auth_views] 
# blueprints must be added to this list
