from string import Template

google_template = Template('''var gaTrackCode = "$tracking_code";
  var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");

  jQuery.getScript(gaJsHost + "google-analytics.com/ga.js", function(){
    var pageTracker = _gat._getTracker(gaTrackCode);
    pageTracker._initData();
    pageTracker._trackPageview();
  }); ''')

color_template = Template('''$$.fn.jPicker.defaults.images.clientPath='http://s3.amazonaws.com/media.webmediaengineering.com/CompoundDoc/images/';
                    $$.fn.jPicker.defaults.window.position.x='0';
                    $$.fn.jPicker.defaults.window.position.y='0';
                    $$('$class_selector').jPicker();''')

tabs_template = Template('''$$("#$tab_id").tabs({cache:false ,ajaxOptions:{cache:false}, cookie:{expires:1}, load: function(event, ui) 
            {$color_picker $nice_submit_button $lightbox} });''')

lightbox_template = Template('''$$("$selector").colorbox({$args});''')

cycle_template = Template('''$$('#$cycle_id').cycle({$args});''')

carousel_template = Template('''$$('#$carousel_id').CloudCarousel({$args});''')

carousel_html_template = Template('''<div id="$carousel_id">$seq</div>$button_left $button_right $title $alt''')

youtube_template = Template('<a href="http://www.youtube.com/embed/$youtube_id?rel=0" rel="$lightbox_id" title="$title"><img src="http://img.youtube.com/vi/$youtube_id/2.jpg"  width="120" height="90" $css_class title="$title"></a>')

def default_javascript(enable_gzip):
    gz = '.gz' if enable_gzip else ''
    return '''<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js"></script>
        <script type="text/javascript" src="http://s3.amazonaws.com/media.webmediaengineering.com/CompoundDoc/default_9{gz}.js"></script>'''.format(gz=gz)

def google_analytics(tracking_code):
    return google_template.substitute(tracking_code=tracking_code)

def color_picker_init(class_selector='.color_picker'):
    return color_template.substitute(class_selector=class_selector)  

def tabs_init(tab_id):
    return tabs_template.substitute(tab_id=tab_id, nice_submit_button=nice_submit_button(), 
        lightbox=lightbox_init(), color_picker=color_picker_init())

def tabs_html(tab_id, tabs):
    tab_format = '<li><a href="%s">%s</a></li>'
    temp = ['<div id="%s"><ul>' % tab_id]
    for url, tab_title in tabs:
        temp.append(tab_format % (url, tab_title))
    temp.append('</ul></div>')
    return ''.join(temp)

def lightbox_init(selector="a[rel^='lightbox']", args=None):
    defaults = {"maxWidth":"'85%'", "maxHeight":"'85%'", "photo":"true"}
    if args is not None:
        defaults.update(args)
    args = ','.join('%s:%s' % (key,value) for key,value in defaults.items())
    return lightbox_template.substitute(selector=selector, args=args)
    
def lightbox_init_youtube(selector="a[rel^='lightbox']", args=None):
    defaults = {"iframe":"true", "onCleanup":"function(){ $('#colorbox iframe').attr('src', 'about:blank'); }"}
    if args is not None:
        defaults.update(args)
    return lightbox_init(selector=selector, args=defaults)
    
def lightbox_html():
    return ''

def nice_submit_button():
    return '$("input:submit").removeClass("submitChanges submit").button();'

def document_ready(seq):
    return '<script type="text/javascript">$(document).ready(function(){' + '\n'.join(seq) +'});</script>'
    
def cycle_init(cycle_id, args=None):
    defaults = {'fx':"'fade'", 'speed':'300', 'timeout':'3000', 'pause':'1'}
    if args is not None:
        defaults.update(args)
    args = ','.join('%s:%s' % (key,value) for key,value in defaults.items())
    return cycle_template.substitute(cycle_id=cycle_id, args=args)

def cycle_html(cycle_id, seq):
    return '<div id="%s">%s</div>' % (cycle_id, ''.join(seq))
 
def cycle_html_youtube(cycle_id, lightbox_id, seq):
    sub = youtube_template.substitute
    seq = [sub(youtube_id=youtube_id, title=title, lightbox_id=lightbox_id, css_class='') for youtube_id, title in seq]
    return cycle_html(cycle_id, seq)

def carousel_init(carousel_id, args=None):
    carousel_ids = carousel_control_ids(carousel_id)
    defaults = {'reflHeight':'56', 'reflGap':'2', 'mouseWheel':'true'}
    defaults['buttonLeft'] = '$("#%s")' % carousel_ids['button_left']
    defaults['buttonRight'] = '$("#%s")' % carousel_ids['button_right']
    defaults['altBox'] = '$("#%s")' % carousel_ids['alt']
    defaults['titleBox'] = '$("#%s")' % carousel_ids['title']
    if args is not None:
        defaults.update(args)
    args = ','.join('%s:%s' % (key,value) for key,value in defaults.items())
    return carousel_template.substitute(carousel_id=carousel_id, args=args)

def carousel_control_ids(carousel_id):
    return {'button_left':'left-button-%s' % carousel_id, 
        'button_right':'right-button-%s' % carousel_id, 
        'alt':'alt-text-%s' % carousel_id, 
        'title':'title-text-%s' % carousel_id}

def carousel_html(carousel_id, seq, args=None):
    defaults = {'button_left':'<input id="%s" type="button" value="Left">', 
        'button_right':'<input id="%s" type="button" value="Right">', 
        'title':'<p id="%s"></p>', 
        'alt':'<p id="%s"></p>'}
    if args is not None:
        defaults.update(args)
    controls = {}
    for key,value in carousel_control_ids(carousel_id).items():
        try:
            controls[key] = defaults[key] % value
        except TypeError:
            controls[key] = ''
    seq = '\n'.join(seq)
    return carousel_html_template.substitute(carousel_id=carousel_id, seq=seq, button_left=controls['button_left'], 
        button_right=controls['button_right'], alt=controls['alt'], title=controls['title'])

def carousel_html_youtube(carousel_id, lightbox_id, seq, args=None):
    sub = youtube_template.substitute
    seq = [sub(youtube_id=youtube_id, title=title, lightbox_id=lightbox_id, css_class='class="cloudcarousel"') for youtube_id, title in seq]
    return carousel_html(carousel_id, seq, args=None)