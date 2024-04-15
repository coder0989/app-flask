from flask import Flask, redirect, url_for, render_template, request, session
import os
from ai.assistant import assist

app=Flask(__name__)
app.secret_key='Ocean007'
assist=assist()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method=='POST':
     name=request.form['nm']
     session['name']=name
     print(name)
     return redirect(url_for('account'))
   else:
     return render_template('login.html')


@app.route('/account')
def account():
  if 'name' in session:
    user=session['name']
    return render_template('account.html', name=user)
  else:
    return redirect(url_for('login'))

@app.route('/AI_choice', methods=['GET', 'POST'])
def AI_choice():
  if 'name' in session:
    if request.method=='POST':
      if 'info' in request.form:
        return redirect(url_for('info'))
      elif 'assist' in request.form:
        return redirect(url_for('assistant'))
      else:
        return redirect(url_for('AI_choice'))
    else:
      return render_template('ai_choice.html')
  else:
    return redirect(url_for('login'))

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/info', methods=['POST', 'GET'])
def info():
  if 'name' in session:
    if request.method=='POST' and request.form['nmm']==os.environ['CODE']:
      session['info']='active'
      return redirect(url_for('realy'))
    else:
      return render_template('info.html')
  else:
    return redirect(url_for('login'))

@app.route('/realy')
def realy():
  if 'info' in session:
    if session['info']=='active':
      return render_template('realy.html')
    else:
      return redirect(url_for('home'))
  else:
    return redirect(url_for('home'))

@app.route('/assistant', methods=['POST', 'GET'])
def assistant():
  if request.method=='POST':
    session['ans']=assist.ask(request.form['question'])
    return redirect(url_for('answer'))
  else:
    return render_template('question.html')

@app.route('/answer', methods=['POST', 'GET'])
def answer():
  if 'ans' in session:
    if request.method=='POST':
      return redirect(url_for('assistant'))
    else:
      return render_template('answer.html', ans=session['ans'])
  else:
    return redirect(url_for('assistant'))
if __name__=='__main__':
  app.run(debug=True)
