# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request, jsonify, redirect, url_for, session
from HotOpinion import app
from database import db
from models import User, Poll, Question, Comment
from datetime import timedelta
import json


@app.before_request
def make_session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.route('/')
def index(page=1):
    total = db.session.query(Poll).count()
    pn = Poll.query.order_by(Poll.id.desc()).paginate(page=page,
                                                      per_page=app.config['POSTS_PER_PAGE'],
                                                      error_out=False
                                                      )
    return render_template(
        'poll.html',
        title='Hot Opinion',
        year=datetime.now().year,
        num_of_pages_per_pagination=app.config['POSTS_PER_PAGE'],
        total=total,
        paginate=pn
    )


@app.route("/dbtest")
def db_test():
    if User.query.all():
        return "It works!"
    else:
        return ":("


@app.route('/admin')
def admin():
    if 'is_superuser' in session and session['is_superuser']:
        return render_template(
            'admin.html'
        )
    else:
        total = db.session.query(Poll).count()
        pn = Poll.query.order_by(Poll.id.desc()).paginate(page=1,
                                                          per_page=app.config['POSTS_PER_PAGE'],
                                                          error_out=False
                                                          )
        return render_template(
            'poll.html',
            title='Hot Opinion',
            year=datetime.now().year,
            num_of_pages_per_pagination=app.config['POSTS_PER_PAGE'],
            total=total,
            paginate=pn
        )


@app.route('/poll_more/<int:page>', methods=['GET', 'POST'])
def more_polls(page):
    pn = Poll.query.order_by(Poll.id.desc()).paginate(page=page,
                                                      per_page=app.config['POSTS_PER_PAGE'],
                                                      error_out=False
                                                      )
    return jsonify(pn)


@app.route('/add_poll', methods=['POST'])
def add_poll():
    if request.method == 'POST':
        subject = request.form['poll_subject']
        statement = request.form['poll_description']
        num_questions = request.form['num_answers']
        int_num_questions = int(num_questions)
        p = Poll(subject=subject,
                 question_statement=statement,
                 num_questions=num_questions)

        for i in range(1, int_num_questions + 1):
            q = Question(choice_num=i,
                         answer_description=request.form['poll_answer'+str(i)]
                         )
            q.poll_id = p.id
            p.questions.append(q)
            db.session.add(q)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/vote', methods=['POST'])
def vote_poll():
    if request.method == 'POST':
        json_data = request.get_json(force=True)
        poll_id = json_data['poll_id']
        choice_id = json_data['choice_id']

        if 'user_email' not in session:
            # Not logged in
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
        user_email = session['user_email']

        u = User.query.filter_by(name_string=user_email).first()
        for each in u.attended_polls:
            if each.id == poll_id:
                print ("Exist!")
                return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

        q = Question.query.get(choice_id)
        q.selected_num += 1
        db.session.merge(q)
        db.session.commit()
        p = Poll.query.get(poll_id)
        p.total_participant += 1
        db.session.merge(p)
        db.session.commit()
        u = User.query.filter_by(name_string=session['user_email']).first()
        p = Poll.query.get(poll_id)
        if p not in u.attended_polls:
            u.attended_polls.append(p)
        User.query.session.commit()
        return json.dumps({'success': True, 'poll_id': p.id}), 200, {'ContentType': 'application/json'}


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        if 'user_email' not in session:
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}

        json_data = request.get_json(force=True)
        poll_id = json_data['poll_id']
        comment = json_data['comment_contents']
        c = Comment(user_name=session['user_name'],
                    comment_content=comment)
        c.poll_id = poll_id
        db.session.add(c)
        db.session.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/modify_delete_poll')
def modify_delete_poll():
    if 'is_superuser' not in session or not session['is_superuser']:
        return redirect(url_for(index))
    total = db.session.query(Poll).count()
    db.session.close()
    pn = Poll.query.order_by(Poll.id.desc()).paginate(page=1,
                                                      per_page=app.config['POSTS_PER_PAGE'],
                                                      error_out=False
                                                      )
    return render_template('delete_modify_poll.html',
                           num_of_pages_per_pagination=app.config['POSTS_PER_PAGE'],
                           total=total,
                           paginate=pn
                           )


@app.route('/modify_poll', methods=['POST'])
def modify_poll_title():
    if request.method == 'POST':
        poll_id = request.form['poll_id']
        modified_title = request.form['modified_title']
        modified_description = request.form['modified_description']
        poll_id = int(poll_id)
        p = Poll.query.filter_by(id=poll_id).first()
        p.subject = modified_title
        p.question_statement = modified_description
        db.session.merge(p)
        db.session.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


@app.route('/modify_questions', methods=['POST'])
def modify_questions():
    if request.method == 'POST':
        poll_id = request.form['poll_id']
        modified_answers = request.form.getlist("modified_answers[]")
        poll_id = int(poll_id)
        questions = Question.query.filter_by(poll_id=poll_id).all()
        for i in range(0, len(questions)):
            questions[i].answer_description = modified_answers[i]
            db.session.merge(questions[i])
            db.session.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/delete_poll', methods=['POST'])
def delete_poll():
    if request.method == 'POST':
        if not session['is_superuser']:
            print("DEBUG: is not super user")
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
        poll_id = request.form['poll_id']
        poll_id = int(poll_id)
        if Poll.query.filter_by(id=poll_id).first() is None:
            # print("DEBUG: poll does not exist")
            json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
        # 1. Comment delete
        try:
            Comment.query.filter_by(poll_id=poll_id).delete()
            Comment.query.session.commit()
            # 2. Question delete
            Question.query.filter_by(poll_id=poll_id).delete()
            Question.query.session.commit()
            # 3. respondents_identifier delete
            p = Poll.query.filter_by(id=poll_id).first()
            print p.User
            user_list = []
            for each_user in p.User:
                user_list.append(each_user)
            print user_list
            for each in user_list:
                each.attended_polls.remove(p)
                User.query.session.commit()
            db.session.commit()
            print "Loop exit"
            # 4. Poll delete
            Poll.query.filter_by(id=poll_id).delete()
            Poll.query.session.commit()
        except:
            db.session.rollback()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}


@app.route('/login_update', methods=['POST'])
def login_process():
    if request.method == 'POST':
        print("POST process is called")
        if 'is_superuser' in session:
            session.pop('is_superuser', None)
        if 'user_email' in session and session['user_email']:
            print("Already Logon")
            print(session['user_email'])
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        json_data = request.get_json(force=True)
        user_email = json_data['user_email']
        user_name = json_data['user_name']

        # User check, if no user, add to database
        u = User.query.filter_by(name_string=user_email).first()
        if u is None:
            # No user exist. Add to Data base
            u = User(name=user_name,
                     name_string=user_email
                     )
            db.session.add(u)
            db.session.commit()

        session['user_name'] = user_name
        session['user_email'] = user_email

        if u.name_string in app.config['SUPER_USER_EMAIL']:
            print("Super user")
            session['is_superuser'] = True
        else:
            print("Not super user")
            session['is_superuser'] = False
        # print("Return Login_Process")
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/logout_update', methods=['POST'])
def logout_process():
    if request.method == 'POST':
        session.clear()
        print("Successfully Log out")
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/init_setting', methods=['POST'])
def init_setting():
    if 'is_superuser' in session:
        session.pop('is_superuser', None)
    if 'user_name' in session:
        session.pop('user_name', None)
    # if 'logged_in' in session:
    #     session['logged_in'] = False
    if 'user_email' in session:
        session.pop('user_email', None)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    if request.method == 'POST':
        print("Delete comment entry")
        if not session['is_superuser']:
            print("Not super_user")
            return json.dumps({'success': False}), 200, {'ContentType': 'application/json'}
        comment_id = request.form['comment_id']
        comment_id = int(comment_id)
        Comment.query.filter_by(id=comment_id).delete()
        Comment.query.session.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
