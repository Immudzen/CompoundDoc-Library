def default_css(enable_gzip, jquery_ui_theme):
    gz = '.gz' if enable_gzip else ''
    return '''<link rel="stylesheet" type="text/css" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/themes/{theme}/jquery-ui.css">
        <link rel="stylesheet" type="text/css" href="http://s3.amazonaws.com/media.webmediaengineering.com/CompoundDoc/default_9{gz}.css">'''.format(gz=gz, theme=jquery_ui_theme)
