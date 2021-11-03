from flask import Blueprint, redirect
from controllers.ViewsController import sign_up, sign_in, redir, home, logout, tasks, tasks_add, tasks_delete

views = Blueprint('views', __name__)



views.route('/', methods=["GET"])(redir)
views.route('/sign_up', methods=["GET", "POST"])(sign_up)
views.route('/sign_in', methods=["GET", "POST"])(sign_in)
views.route('/home', methods=["GET"])(home)
views.route('/logout', methods=["GET"])(logout)
views.route('/tasks', methods=["GET"])(tasks)
views.route('/tasks/add', methods=["POST"])(tasks_add)
views.route('/tasks/delete', methods=["POST"])(tasks_delete)
