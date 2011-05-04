allowed_themes = set(['base', 'black-tie', 'blitzer', 'cupertino', 'dark-hive', 'dot-luv', 'eggplant',
        'excite-bike', 'flick', 'hot-sneaks', 'humanity', 'le-frog', 'mint-choc',
        'overcast', 'pepper-grinder', 'redmond', 'smoothness', 'south-street',
        'start', 'sunny', 'swank-purse', 'trontastic', 'ui-darkness', 'ui-lightness', 'vader'])


def default_css(enable_gzip, jquery_ui_theme):
    """This function takes two arguements one is if gzip should be enabled
    with a True or False value and what jquery ui theme to use
    Valid values for jquery_ui_theme are:
        'base', 'black-tie', 'blitzer', 'cupertino', 'dark-hive', 'dot-luv', 'eggplant',
        'excite-bike', 'flick', 'hot-sneaks', 'humanity', 'le-frog', 'mint-choc',
        'overcast', 'pepper-grinder', 'redmond', 'smoothness', 'south-street',
        'start', 'sunny', 'swank-purse', 'trontastic', 'ui-darkness', 'ui-lightness', 'vader'
    It then includes the latest version of jquery ui css from the google cdn and the combined css on amazon
    """
    gz = '.gz' if enable_gzip else ''
    jquery_ui_theme = jquery_ui_theme if jquery_ui_theme in allowed_themes else 'base'
    return '''<link rel="stylesheet" type="text/css" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/themes/{theme}/jquery-ui.css">
        <link rel="stylesheet" type="text/css" href="http://s3.amazonaws.com/media.webmediaengineering.com/CompoundDoc/default_9{gz}.css">'''.format(gz=gz, theme=jquery_ui_theme)
