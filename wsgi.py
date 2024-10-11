import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from sqlalchemy.exc import IntegrityError

from App.database import db, get_migrate
from App.models import User, Student, Review
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize,  create_student, get_student_by_lName, get_all_students , create_review)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@app.cli.command('create-student', help="Creates a student")
@click.argument('fname', default='rob')
@click.argument('lname', default='robbington')
def create_student_command(fname,lname):
  create_student(fname, lname)
  print(f'{fname} {lname} created!')

@app.cli.command('get-student', help="Retrieves a Student")
@click.argument('lname', default='bobbington')
def get_student(lname):
  bob = get_student_by_lName(lname)
  if not bob:
    print(f'{lname} not found!')
    return
  print(bob)

@app.cli.command('get-students')
def get_students():
  # gets all objects of a model
  students = get_all_students()
  print(students)

@app.cli.command('get-reviews')
@click.argument('lname', default='bobbington')
def get_user_todos(lname):
  bob = get_student_by_lName(lname)
  if not bob:
      print(f'{lname} not found!')
      return
  print(bob.reviews)

@app.cli.command('add-review')
@click.argument('lname', default='bobbington')
@click.argument('title', default='Excellent Work')
@click.argument('text', default='Has topped the class')
def add_review(lname, title, text):
  bob = get_student_by_lName(lname)
  if not bob:
      print(f'{username} not found!')
      return
  create_review(bob, title, text)
  print(f'Review\nTitle:{title}\nText:{text}\nStudent:{lname}\ncreated!')

@app.cli.command('add-review2')
@click.argument('lname', default='robbington')
@click.argument('title', default='Inappropriate Misconduct')
@click.argument('text', default='Very distractive and talkative in class')
def add_review(lname, title, text):
  bob = get_student_by_lName(lname)
  if not bob:
      print(f'{username} not found!')
      return
  create_review(bob, title, text)
  print(f'Review\nTitle:{title}\nText:{text}\nStudent:{lname}\ncreated!')


@app.cli.command('get-all-reviews')
def get_students():
  # gets all objects of a model
  students = get_all_students()
  for x in students:
    print(x.reviews)
    print('\n')
  #print(students.reviews)


# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)