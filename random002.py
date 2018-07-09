from celery import Celery
import requests

app = Celery('random002', broker='redis://185.111.73.117:6379/0')


@app.task
def fetch_url(url):
    resp = requests.get(url)
    print(resp.status_code)


def func(urls):
    for url in urls:
        print('Working on %s' % url)
        fetch_url.delay(url)


if __name__ == "__main__":
    func(["http://google.com", "https://amazon.in", "https://facebook.com",
          "https://twitter.com", "https://alexa.com"])
