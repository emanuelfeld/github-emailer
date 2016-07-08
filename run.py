import os
import sys
import logging
from datetime import date, timedelta

import requests
import sendgrid
from sendgrid.helpers.mail import *
from jinja2 import Environment, FileSystemLoader


def send_email(body, subject, fromaddr, toaddr, apikey):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(fromaddr)
    to_email = Email(toaddr)
    content = Content("text/html", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code >= 400:
        raise IOError('Status code', response.status_code)


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
        count = 0
        if data['total_count'] > 0:
            for repository in data['items']:
                out[repository['name']] = {
                    'repo_url': repository['html_url'],
                    'description': repository['description'],
                    'homepage': repository['homepage']
                }
                count += 1
        logger.info('{organization}: {count} new repositories found'.format(
            organization=organization, count=count))
    except:
        logger.warning('{organization} could not be accessed'.format(
            organization=organization))
    return out


def get_following(gist_id):
    response = requests.get('https://gist.github.com/raw/{id}'.format(id=gist_id))
    following = response.text.splitlines()
    logger.info('Following {} organizations'.format(len(following)))
    return following


if __name__ == '__main__':
    if str(date.today().weekday()) == os.environ.get('UPDATE_DAY'):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        output = {}
        from_date = date.today() - timedelta(7)
        base_url = 'https://api.github.com/search/repositories?access_token={token}&q=user:{user}+created:>={date}'
        token=os.environ.get('GITHUB_TOKEN')
        following = get_following(os.environ.get('GIST_ID'))

        for organization in following:
            updates = get_updates(organization, from_date, token, base_url)
            if updates:
                output[organization] = updates

        message = format_email(output)
        logger.info('Email formatted')

        try:
            send_email(body=message,
                       subject="GitHub Updates for the Week of {}".format(from_date),
                       fromaddr=os.environ.get('FROM_ADDR'),
                       toaddr=os.environ.get('TO_ADDR'),
                       apikey=os.environ.get('SENDGRID_API_KEY'))
            logger.info('Email sent')
        except Exception as e:
            logger.error('Failed to send email: {}'.format(e))
            raise
