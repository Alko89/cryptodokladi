from .rules import (
    send_funds_factory,
    page_factory,
    new_page_factory,
    user_list_factory,
    calculate_staking_rewards,
    user_change_settings,
    user_factory,
    add_funds_factory
)

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_wiki', '/')
    config.add_route('solidity', '/solidity')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    
    config.add_route('limit_trade', '/limit_trade', factory=send_funds_factory)

    config.add_route('songs_list', 'song')
    config.add_route('tag', '/song/tag/{tagname}')
    config.add_route('song_add', '/song/add')
    config.add_route('song_edit', '/song/{songtitle}/edit')
    config.add_route('song', '/song/{songtitle}')

    config.add_route('view_page', '/{pagename}', factory=page_factory)
    config.add_route('add_page', '/add_page/{pagename}', factory=new_page_factory)
    config.add_route('edit_page', '/{pagename}/edit_page', factory=page_factory)

    config.add_route('user_list', '/user/user_list', factory=user_list_factory)
    config.add_route('user_new', '/user/user_new', factory=user_list_factory)
    config.add_route('add_multiple_funds', '/user/add_multiple_funds', factory=calculate_staking_rewards)
    config.add_route('user_settings', '/user/settings/{username}', factory=user_change_settings)
    config.add_route('user_settings_save', '/user/settings/{username}/save', factory=user_change_settings)
    config.add_route('user_view', '/user/{username}', factory=user_factory)
    config.add_route('add_funds', '/user/add_funds/{username}', factory=add_funds_factory)
    config.add_route('send_funds', '/user/send_funds/{username}', factory=send_funds_factory)

    config.add_route('calculate_staking_rewards', '/api/calculate_rewards/{pivx_reward}/{comment}/{save}', factory=calculate_staking_rewards)
    config.add_route('add_multiple_funds_call', '/api/add_multiple_funds_call/{token}/{rate}', factory=calculate_staking_rewards)
    config.add_route('user_transactions', '/api/user_transactions/{username}', factory=user_factory)
    config.add_route('eur_usd_rate', '/api/eur_usd_rate')
    
    config.add_route('home', '/api/home')
    config.add_route('get_tokens', '/api/tokens')
