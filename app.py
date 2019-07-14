from flask import flash, Flask, g, redirect, render_template, url_for
from flask_bcrypt import check_password_hash
from flask_login import (current_user, login_required, login_user, logout_user,
                         LoginManager)

from slugify import slugify

from peewee import *

from forms import EntryForm, LoginForm, RegisterForm
from models import db, Entry, EntryTags, initialize, Tag, User

import testdata


DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = b'\xdb4\xe8@Y\xa7\xaaR\x8a\x8dX\xc5\xe4\xe7L\x1c'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before each request."""
    g.db = db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/<int:tag_id>')
@app.route('/entries')
def index(tag_id=None):
    if tag_id:
        tag = Tag.select().where(Tag.id == tag_id).get()
        entries = tag.get_entries()
    else:
        entries = Entry.select()
    return render_template('index.html', entries=entries)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            login_user(user)
            return redirect(url_for('index'))
        except (IntegrityError, ValueError) as e:
            flash(e)
    else:
        flash_errors(form)
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash("Your email or password doesn't match!")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!")
    else:
        flash_errors(form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def create():
    form = EntryForm()
    if form.validate_on_submit():
        try:
            entry = Entry.create(
                title=form.title.data,
                date=form.date.data,
                time=form.time.data,
                learned=form.learned.data,
                resources=form.resources.data,
                slug=safe_slugify(form.title.data),
                user=g.user.id
            )
            process_tags(form.tags.data, entry)
        except IntegrityError:
            flash("An entry with that title already exists.")
        else:
            return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template('new.html', form=form)


@app.route('/entries/<slug>')
def detail(slug):
    entry = Entry.get(Entry.slug == slug)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<slug>/edit', methods=('GET', 'POST'))
@login_required
def edit(slug):
    entry = Entry.get(Entry.slug == slug)
    if entry.user == g.user or g.user.is_admin:
        form = EntryForm()
        if form.validate_on_submit():
            try:
                entry.title = form.title.data
                entry.date = form.date.data
                entry.time = form.time.data
                entry.learned = form.learned.data
                entry.resources = form.resources.data
                entry.slug = safe_slugify(form.title.data, entry)
                entry.save()
                if form.tags.data:
                    # clear and refresh tags in case any were removed
                    clear_tags(entry)
                    process_tags(form.tags.data, entry)
                flash("Entry updated successfully.")
                return redirect(url_for('detail', slug=entry.slug))
            except IntegrityError:
                flash("An entry with that title already exists.")
        else:
            flash_errors(form)
    else:
        # this should only be reached if user directly enters in url, as edit
        # link should not display if logged in user did not create entry
        return ("You know, it's really not nice to try to edit things that do "
                "not belong to you.")
    return render_template('edit.html', entry=entry, form=form)


@app.route('/entries/<slug>/delete')
@login_required
def delete(slug):
    entry = Entry.get(Entry.slug == slug)
    if entry.user == g.user or g.user.is_admin:
        entry.delete_instance()
        flash("Entry deleted successfully.")
        return redirect(url_for('index'))
    else:
        # this should only be reached if user directly enters in url, as button
        # should not display if logged in user did not create entry
        return "This is not my sandwich. Nice try, scumbag."


def clear_tags(entry):
    entry_tags = EntryTags.select().where(EntryTags.entry == entry)
    for entry_tag in entry_tags:
        entry_tag.delete_instance()


def process_tags(tags, entry):
    tags = tags.split()
    if tags:
        for tag in tags:
            try:
                tag = Tag.create(tag_name=tag)
            except IntegrityError:
                tag = Tag.select().where(Tag.tag_name == tag).get()
            try:
                EntryTags.create(entry=entry, tag=tag)
            except IntegrityError:
                pass


def safe_slugify(title, current_entry=None):
    """Appends entry id to slug in case conflicts arise due to
    alternate title capitalization or punctuation."""
    slug = slugify(title)
    if current_entry and current_entry.slug == slug:
        return slug
    else:
        entries = Entry.select()
        slugs = [entry.slug for entry in entries]
        if slug in slugs:
            if current_entry:
                slug += "~" + str(current_entry.id)
            else:
                slug += "~" + str(entries[-1].id + 1)
        return slug


def flash_errors(form):
    for item in form.errors.items():
        flash(item[1][0])


@app.template_filter()
def pluralize(num, singular='', plural='s'):
    if num == 1:
        return singular
    else:
        return plural


if __name__ == '__main__':
    initialize()
    if not User.select():
        for data in testdata.test_users:
            try:
                User.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    is_admin=data['is_admin']
                )
            except (IntegrityError, ValueError):
                pass

    if not Entry.select():
        for data in testdata.test_entries:
            entry = Entry.create(
                title=data['title'],
                time=data['time'],
                learned=data['learned'],
                resources=data['resources'],
                slug=safe_slugify(data['title']),
                user=data['user_id']
            )
            if 'tags' in data:
                process_tags(data['tags'], entry)

    app.run(debug=DEBUG, host=HOST, port=PORT)
