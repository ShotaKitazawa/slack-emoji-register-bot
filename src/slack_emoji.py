from bs4 import BeautifulSoup
from robobrowser import RoboBrowser


def upload_emoji(session, emoji_name, filename):
    # Fetch the form first, to generate a crumb.
    r = session.get(session.url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    crumb = soup.find("input", attrs={"name": "crumb"})["value"]

    data = {
        'add': 1,
        'crumb': crumb,
        'name': emoji_name,
        'mode': 'data',
    }
    files = {'img': open(filename, 'rb')}
    r = session.post(session.url, data=data,
                     files=files, allow_redirects=False)
    r.raise_for_status()
    # Slack returns 200 OK even if upload fails,
    # so check for status of 'alert_error' info box
    if b'alert_error' in r.content:
        soup = BeautifulSoup(r.text, "html.parser")
        crumb = soup.find("p", attrs={"class": "alert_error"})
        raise ValueError("Error with uploading %s: %s"
                         % (emoji_name, crumb.text))


class EmojiUploader(object):
    def __init__(self, workspace, email, password):
        url = 'https://{}.slack.com/admin/emoji'.format(workspace)

        browser = RoboBrowser(parser='html.parser', history=True)
        browser.open(url)
        form = browser.get_form(action='/')
        form['email'] = email
        form['password'] = password
        browser.submit_form(form)

        self.session = browser.session
        self.session.url = url

    def upload(self, emoji_name, fname):
        upload_emoji(self.session, emoji_name, fname)


if __name__ == '__main__':
    import os
    email = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    workspace = os.environ['WORKSPACE']
    uploader = EmojiUploader(workspace, email, password)
    uploader.upload('aaatest', './tetris_purple.png')
