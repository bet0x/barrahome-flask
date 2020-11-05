import os
import re
import mistune
import collections
import time
import yaml
from functools import wraps
from datetime import datetime, date, timedelta
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from flask import render_template, send_from_directory, make_response, Response, json
from wsgiref.handlers import format_date_time
from website import app

with open('config/website.yaml') as f:    
    data = yaml.load(f, Loader=yaml.FullLoader)

class Post:
    def __init__(self, title, date, tags, summary, author, href, content_md):
        self.title = title
        self.date = date
        self.tags = tags
        self.summary = summary
        self.author = author
        self.href = href
        self.content_md = content_md
        self.content_html = md_to_html(content_md)


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
    
def cache(expires=None, round_to_minute=False):
    def cache_decorator(view):
        @wraps(view)
        def cache_func(*args, **kwargs):
            now = datetime.now()
            response = make_response(view(*args, **kwargs))
            response.headers['Last-Modified'] = format_date_time(time.mktime(now.timetuple()))
            if expires is None:
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
                response.headers['Expires'] = '-1'
            else:
                expires_time = now + timedelta(seconds=expires)
                if round_to_minute:
                    expires_time = expires_time.replace(second=0, microsecond=0)
                response.headers['Cache-Control'] = 'public'
                response.headers['Expires'] = format_date_time(time.mktime(expires_time.timetuple()))
            return response
        return cache_func
    return cache_decorator

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_service_error(e):
    return render_template('500.html'), 500

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    pages.append([data['website']['address'], '2018-07-21'])
    pages.append([data['website']['address'], '2018-07-21'])
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        url = data['website']['address'] + '%s' % file.replace('.md', '')
        last_mod = post_obj.date
        pages.append([url, last_mod])
    response= make_response(render_template("sitemap.xml", pages=pages))
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/legal')
@cache(expires=60)
def legal():
    return render_template('legal.html')

@app.route('/credits')
@cache(expires=60)
def credits():
    return render_template('credits.html')

@app.route('/contact')
@cache(expires=60)
def contact():
    return render_template('contact.html')

@app.route('/projects')
@cache(expires=60)
def projects():
    return render_template('projects.html')    

@app.route('/')
@cache(expires=None)
def index():
    tag_dict = dict()
    posts = []
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        posts.append(post_obj)
        for tag in post_obj.tags:
            if tag not in tag_dict.keys():
                tag_dict[tag] = 0
            tag_dict[tag] += 1
    sorted_tag_dict = collections.OrderedDict()
    for key in sorted(tag_dict.keys()):
        sorted_tag_dict[key] = tag_dict[key]
    sorted_posts = sorted(posts, 
        key=lambda x: datetime.strptime(x.date, '%Y-%m-%d'), reverse=True)
    return render_template('articles.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict)


@app.route('/articles/tag/<queried_tag>')
@cache(expires=None)
def get_tagged_posts(queried_tag):
    tag_dict = dict()
    matching_posts = []
    content_path = os.path.join(app.root_path, 'content')
    for file in os.listdir(content_path):
        if not file.endswith('.md'):
            continue
        full_path = os.path.join(content_path, file)
        post_obj = parse_markdown_post(full_path)
        if queried_tag in post_obj.tags:
            matching_posts.append(post_obj)
        for tag in post_obj.tags:
            if tag not in tag_dict.keys():
                tag_dict[tag] = 0
            tag_dict[tag] += 1
    sorted_tag_dict = collections.OrderedDict()
    for key in sorted(tag_dict.keys()):
        sorted_tag_dict[key] = tag_dict[key]
    sorted_posts = sorted(matching_posts,
        key=lambda x: datetime.strptime(x.date, '%Y-%m-%d'), reverse=True)
    return render_template('articles.html', posts=sorted_posts,
        tag_dict=sorted_tag_dict, queried_tag=queried_tag)


@app.route('/article/<post_title>')
@cache(expires=None)
def blog_post(post_title):
    try:
        md_path  = os.path.join(app.root_path, 'content', '%s.md' % post_title)
        print (md_path)
        post = parse_markdown_post(md_path)
        return render_template('article.html', post=post)
    except IOError:
        return render_template('404.html'), 404


def parse_markdown_post(md_path):
    with open(md_path, 'rU') as f:
        markdown = f.read()
    re_pat = re.compile(r'title: (?P<title>[^\n]*)\sdate: (?P<date>\d{4}-\d{2}-\d{2})\s'
                        r'tags: (?P<tags>[^\n]*)\ssummary: (?P<summary>[^\n]*)\sauthor: (?P<author>[^\n]*)\s')
    match_obj = re.match(re_pat, markdown)
    title = match_obj.group('title')
    date = match_obj.group('date')
    summary = match_obj.group('summary')
    author = match_obj.group('author')
    tags = sorted([tag.strip() for tag in match_obj.group('tags').split(',')])
    href = os.path.join(data['website']['address'], 'article', title.lower().replace(' ', '-'))
    content_md = re.split(re_pat, markdown)[-1]
    return Post(title, date, tags, summary, author, href, content_md)


def md_to_html(md_string):
    markdown_formatter = mistune.Markdown(renderer=HighlightRenderer(parse_block_html=True))
    html = markdown_formatter(md_string)
    return html
