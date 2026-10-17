type Video = dict[str, str]

VIDEO_FORMAT = lambda title=None, description=None, link=None, published=None: {
    "title": title,
    "description": description,
    "link": link,
    "published": published,
}
