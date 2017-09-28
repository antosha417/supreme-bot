"""Authorizetion wia vk."""
import json
import urllib2

from flask import redirect, request, url_for

import models
from app import app, db
from config import APP_ID, APP_SECRET_KEY, REDIRECT_URL, session, user_loggined


@app.route('/begin', methods=['GET', 'POST'])
def begin():
    """Redirect to vk login page."""
    if user_loggined():
        return redirect(url_for('index') + '#whatis')
    url = 'https://oauth.vk.com/authorize?response_type=code&v=5.60&client_id='
    url += APP_ID + '&redirect_uri=' + REDIRECT_URL + '#whatis'
    return redirect(url)


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    """Take from vk information about user."""
    if request.method == 'GET':
        code = request.args.get('code')
        if code is not None:
            url = 'https://oauth.vk.com/access_token?client_id=' + APP_ID + \
                  '&client_secret=' + APP_SECRET_KEY + \
                  '&redirect_uri=' + REDIRECT_URL + '&code=' + code
            data = json.loads(urllib2.urlopen(url).read())
            u_id = data.get('user_id')
            if u_id is not None:
                url = 'https://api.vk.com/method/users.get?user_ids=' + \
                      str(u_id) + '&v=5.60'
                data = json.loads(urllib2.urlopen(url).read())
                response = data.get('response')
                last_name = data.get('response')[0].get('last_name')
                first_name = data.get('response')[0].get('first_name')
                if response is not None and \
                   last_name is not None and \
                   first_name is not None:
                    u_name = data['response'][0]['last_name'] + ' ' + \
                             data['response'][0]['first_name']
                    if len(u_name) > 40:
                        u_name = data['response'][0]['first_name']

                    user = models.User.query.get(u_id)
                    if user is None:
                        u = models.User(id=int(u_id), name=u_name[:19])
                        db.session.add(u)
                        db.session.commit()

                    session['logged_in'] = True
                    session['user_id'] = int(u_id)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Logout user."""
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))

