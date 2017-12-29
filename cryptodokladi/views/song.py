from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import view_config
from sqlalchemy import func

from ..models import Song, Lyric, Tag

@view_config(route_name='songs_list', renderer='../templates/songs_list.jinja2')
def songs_list(request):
    songs = request.dbsession.query(Song).order_by(Song.title).all()

    return dict(songs=songs)

@view_config(route_name='tag', renderer='../templates/songs_list.jinja2')
def tag(request):
    text = request.matchdict['tagname']
    songs = request.dbsession.query(Tag).filter_by(text=text).first().songs

    return dict(songs=songs)

@view_config(route_name='song', renderer='../templates/song.jinja2')
def song(request):
    title = request.matchdict['songtitle']
    song = request.dbsession.query(Song).filter_by(title=title).first()
    if song is None:
        raise HTTPNotFound('No such song')
    
    edit_url = request.route_url('song_edit', songtitle=song.title)
    return dict(song=song, edit_url=edit_url)

@view_config(route_name='song_edit', renderer='../templates/song_edit.jinja2')
def song_edit(request):
    title = request.matchdict['songtitle']
    song = request.dbsession.query(Song).filter_by(title=title).one()
    user = request.user
    if user is None or (user.role != 'editor'):
        raise HTTPForbidden

    if 'form.submitted' in request.params:
        song.title = request.params['title']
        song.subtitle = request.params['subtitle']
        song.ytplayer = request.params['ytplayer']
        song.tags = get_tag_list(request)
        
        for lyric in song.lyrics:
            if lyric.language == 'text':
                lyric.text = request.params['lyric_text']
            if lyric.language == 'en':
                lyric.text = request.params['lyric_en']
            if lyric.language == 'ru':
                lyric.text = request.params['lyric_ru']
        
        next_url = request.route_url('song', songtitle=song.title)
        return HTTPFound(location=next_url)

    edit_url = request.route_url('song_edit', songtitle=song.title)
    return dict(song=song, edit_url=edit_url)

@view_config(route_name='song_add', renderer='../templates/song_add.jinja2')
def song_add(request):
    user = request.user
    if user is None or user.role not in ('editor'):
        raise HTTPForbidden

    if 'form.submitted' in request.params:
        title = request.params['title']
        subtitle = request.params['subtitle']
        ytplayer = request.params['ytplayer']
        tags = get_tag_list(request)
        
        song = Song(title=title, subtitle=subtitle, ytplayer=ytplayer, tags=tags)
        
        song.lyrics.append(Lyric(language='text', text=request.params['lyric_text']))
        song.lyrics.append(Lyric(language='en', text=request.params['lyric_en']))
        song.lyrics.append(Lyric(language='ru', text=request.params['lyric_ru']))
        
        request.dbsession.add(song)
        next_url = request.route_url('song', songtitle=song.title)
        return HTTPFound(location=next_url)

    edit_url = request.route_url('song_add')
    return dict(edit_url=edit_url)
    

def get_tag_list(request):
    """Get a string of space sperated tag,
    and returns a list of tag objects"""
    taglist = []

    tags = request.params['tags'].strip().split("#")
    tags = set(tags) # no duplicates!

    for tag in tags:
        if len(tag) > 3:
            tag = "#" + tag.strip()
            tagobj = request.dbsession.query(Tag).filter_by(text=tag).first()
            if tagobj is None:
                tagobj = Tag(text=tag)
            taglist.append(tagobj)

    return taglist
