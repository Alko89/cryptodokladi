import os
import sys
import transaction

import json

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Song, Lyric, Tag, Page, User, Funds


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        jaka7 = User(name='7jaka7', role='editor')
        jaka7.set_password('editor')
        dbsession.add(jaka7)

        alko = User(name='alko', role='basic')
        alko.set_password('mojamama')
        dbsession.add(alko)

        page = Page(
            name='FrontPage',
            title='Prva Stran',
            subtitle='Dobrodosli',
            creator=jaka7,
            data='Novice o Kripto Kojnih.',
        )
        dbsession.add(page)

        about = Page(
            name='About',
            title='O Nas',
            subtitle='O Nas',
            creator=alko,
            data='GoOpen',
        )
        dbsession.add(about)

        with open('./cryptodokladi/scripts/capoeiralyrics_2017-12-18.json') as data_file:    
            data = json.load(data_file)
        
        for song in data:
            s = Song(title = song['title'],
                    subtitle = song['subtitle'])
            
            if song['ytplayer'] is not None:
                s.ytplayer = song['ytplayer']
            
            dbsession.add(s)
            
            for key in song['lyrics'].keys():
                
                l = Lyric(language=key, text=song['lyrics'][key].replace('\n', '<br />'), song=s)
                
                dbsession.add(l)
        
        
        with open('./cryptodokladi/scripts/tags_2017-12-18.json') as data_file:    
            data = json.load(data_file)
            
        for s in data:
            song = dbsession.query(Song).filter_by(title=s['title']).first()
            if song is not None:
            
                for t in s['tags']:
                    tag = dbsession.query(Tag).filter_by(text=t).first()
                    if tag is None:
                        tag = Tag(text = t)
                        dbsession.add(tag)
                    
                    song.tags.append(tag)
