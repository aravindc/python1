"""An example of writing an API to scrape hacker news once, and then enabling usage everywhere"""
import hug
import requests


@hug.local()
@hug.cli()
@hug.get()
def top_post(section: hug.types.one_of(('news', 'newest', 'show'))='news'):
    """Returns the top post from the provided section"""
    content = requests.get('https://news.ycombinator.com/{0}'.format(section)).content
    text = content.decode('utf-8')
    print(text)
    return text.split('<tr class=\'athing\'>')[1].split("<a href")[1].split(">")[1].split("<")[0]


@hug.get('/happy_birthday', examples="name=HUG&age=1")
def happy_birthday(name: hug.types.text, age: hug.types.number):
    """Says happy birthday to a user"""
    return "Happy {0} Birthday {1}!".format(name, age)
