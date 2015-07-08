from urlparse import urljoin


def add_slug_to_hackpad_url(slug):
    return urljoin('https://hki.hackpad.com/', slug)
