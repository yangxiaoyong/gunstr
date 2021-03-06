# -*- encoding:utf-8 -*-

import markdown
import os.path
import re
import logging
import time

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from models import SqliteModel

from tornado.options import define, options

cwd = os.path.dirname(__file__)

define("port", default=8888, help="run on the given port", type=int)
define("sqlite_db", default="%s" % os.path.join(cwd, 'blog.db'), help="blog database")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/archive", ArchiveHandler),
            (r"/feed", FeedHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/compose", ComposeHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            debug = True,
            blog_title=u"YXY Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = SqliteModel(options.sqlite_db)
        # self.db.executescript('init.sql')


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM users WHERE id = ?", int(user_id))


class HomeHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 5")
        if not entries:
            self.redirect("/compose")
            return
        self.render("home.html", entries=entries)


class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = self.db.get("SELECT * FROM entries WHERE slug = ?", slug)
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


class ArchiveHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC")
        self.render("archive.html", entries=entries)


class FeedHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = ?", int(id))
        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = ?", int(id))
            if not entry: raise tornado.web.HTTPError(404)
            slug = entry.slug
            self.db.execute(
                "UPDATE entries SET title = ?, markdown = ?, html = ? "
                "WHERE id = ?", title, text, html, int(id))
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = "entry"
            while True:
                e = self.db.get("SELECT * FROM entries WHERE slug = ?", slug)
                if not e: break
                slug += "-2"
            utc_timestamp = time.time()
            self.db.execute(
                "INSERT INTO entries (author_id,title,slug,markdown,html,"
                "published) VALUES (?,?,?,?,?,%s)" % utc_timestamp,
                self.current_user.id, title, slug, text, html)
        self.redirect("/entry/" + slug)


class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if username is not None:
            ret = self.db.get('SELECT id,password from users WHERE name = ?',
                                 username)
            logging.error('ret: %s' % str(ret))
            if ret:
                if ret['password'] == password:
                    self.set_secure_cookie("user", str(ret['id']))

        self.redirect(self.get_argument("next", "/"))

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
