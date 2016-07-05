import os 
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import date, timedelta

import requests
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv, find_dotenv


def send_email(body, subject, fromaddr, frompw, toaddr):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
     
    msg.attach(MIMEText(body, 'html'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, frompw)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def format_email(data):
    path = os.path.dirname(os.path.realpath(__file__))
    env = Environment(loader=FileSystemLoader('{path}/templates'.format(path=path)))
    template = env.get_template('template.html')
    return template.render(data=data)


def get_updates(organization, from_date, token, base_url):
    out = {}
    url = base_url.format(
            user=organization,
            date=from_date,
            token=token
        )
    response = requests.get(url)
    try:
        data = response.json()
        if data['total_count'] > 0:
            for repository in data['items']:
                out[repository['name']] = {
                    'repo_url': repository['html_url'],
                    'description': repository['description'],
                    'homepage': repository['homepage']
                }
    except:
        pass
    return out


def get_following(gist_id):
    response = requests.get('https://gist.github.com/raw/{id}'.format(id=gist_id))
    return response.text.splitlines()


if __name__ == '__main__':
    output = {}
    from_date = date.today() - timedelta(7)
    base_url = 'https://api.github.com/search/repositories?access_token={token}&q=user:{user}+created:>={date}'
    token=os.environ.get('GITHUBTOKEN')
    following = get_following(os.environ.get('GISTID'))

    for organization in following:
        updates = get_updates(organization, from_date, token, base_url)
        if updates:
            output[organization] = updates

    message = format_email(output)
    send_email(body=message, 
               fromaddr=os.environ.get('FROMADDR'), 
               frompw=os.environ.get('FROMPWD'), 
               toaddr=os.environ.get('TOADDR'), 
               subject="GitHub Updates for the Week of {}".format(from_date))

