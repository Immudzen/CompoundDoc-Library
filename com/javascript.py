from string import Template

google_template = Template('''var gaTrackCode = "$tracking_code";
  var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");

  jQuery.getScript(gaJsHost + "google-analytics.com/ga.js", function(){
    var pageTracker = _gat._getTracker(gaTrackCode);
    pageTracker._initData();
    pageTracker._trackPageview();
    pageTracker._trackPageLoadTime();
  }); ''')

range_template = Template('''$$('#$start_id').attr('readonly', 'readonly');$$('#$stop_id').attr('readonly', 'readonly');
$$("#$slider_id").slider({
            range: true,
            min: $min_value,
            max: $max_value,
            values: [ $start_value, $stop_value ],
            step:$step,
            slide: function( event, ui ) {
                $$( "#$start_id" ).val(ui.values[ 0 ] );
                $$( "#$stop_id" ).val(ui.values[ 1 ] );
            }
        });
''')


color_template = Template('''$$.fn.jPicker.defaults.images.clientPath='http://s3.amazonaws.com/media.webmediaengineering.com/CompoundDoc/images/';
                    $$.fn.jPicker.defaults.window.position.x='0';
                    $$.fn.jPicker.defaults.window.position.y='0';
                    $$('$class_selector').jPicker();''')

tabs_template = Template('''$$("#$tab_id").tabs({cache:false ,ajaxOptions:{cache:false}, load: function(event, ui) 
            {$color_picker $nice_submit_button $lightbox} });''')

lightbox_template = Template('''$$("$selector").colorbox({$args});''')

cycle_template = Template('''$$('#$cycle_id').cycle({$args});''')

carousel_template = Template('''$$('#$carousel_id').CloudCarousel({$args});''')

carousel_html_template = Template('''<div id="$carousel_id">$seq</div>$button_left $button_right $title $alt''')

youtube_template = Template('<a href="http://www.youtube.com/embed/$youtube_id?rel=0" rel="$lightbox_id" title="$title"><img src="http://img.youtube.com/vi/$youtube_id/2.jpg"  width="120" height="90" $css_class title="$title"></a>')

def default_javascript(enable_gzip):
    """include the latest version of jquery, jquery ui and the combined js file
    This function takes two arguements one is if gzip should be enabled"""
    gz = '.gz' if enable_gzip else ''
    return '''<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js"></script>
        <script type="text/javascript" src="http://s3.amazonaws.com/media.webmediaengineering.com/CompoundDoc/default_9{gz}.js"></script>'''.format(gz=gz)

def google_analytics(tracking_code):
    """create google analystics tracking code on a site that can be lazy loaded 
    inside a document ready function, takes the tracking code as a required arguement"""
    return google_template.substitute(tracking_code=tracking_code)

def color_picker_init(class_selector='.color_picker'):
    "create the javascript for a color picker, can use a different class_selector"
    return color_template.substitute(class_selector=class_selector)  

def tabs_init(tab_id):
    """create jquery tabs with the given tab_id, this function takes care to reinit all the normal stuff
    we do on each tab"""
    return tabs_template.substitute(tab_id=tab_id, nice_submit_button=nice_submit_button(), 
        lightbox=lightbox_init(), color_picker=color_picker_init())

def tabs_html(tab_id, tabs):
    """create ajax tabs with the given tab_id
    the format of tabs is a sequence of (url, tab titles)"""
    tab_format = '<li><a href="%s">%s</a></li>'
    temp = ['<div id="%s"><ul>' % tab_id]
    for url, tab_title in tabs:
        temp.append(tab_format % (url, tab_title))
    temp.append('</ul></div>')
    return ''.join(temp)

def tabs_html_data(tab_id, tabs):
    """create static tabs with the given tab_id
    the format is a sequence of (content, tab titles)"""
    tab_title_format = '<li><a href="#tabs-%s">%s</a></li>'
    tab_data_format = '<div id="tabs-%s">%s</div>'
    temp = ['<div id="%s"><ul>' % tab_id]
    titles = []
    data = []
    for idx, (content, tab_title) in enumerate(tabs):
        titles.append(tab_title_format % (idx, tab_title))
        data.append(tab_data_format % (idx, content))
    temp.extend(titles)
    temp.append('</ul>')
    temp.extend(data)    
    temp.append('</div>')
    return ''.join(temp)

def accordion_init(accordion_id):
    "create the jquery accordion with the given id"
    return '$("#%s").accordion({ autoHeight:false });' % accordion_id
    
def accordion_html(accordion_id, tabs):
    """create the accordion html with the given id
    the format of the sequence is (content, title)"""
    tab_format = '<h3><a href="#">%s</a></h3><div>%s</div>'
    temp = ['<div id="%s">' % accordion_id]
    for content, title in tabs:
        temp.append(tab_format % (title, content))
    temp.append('</div>')
    return ''.join(temp)

def range_init(start_id, start_value, stop_id, stop_value, slider_id, min_value, max_value, step):
    """Create a slider object, the slider will set the controls for start and stop value to readonly
    so they can't be changed except with the slider. The arguements are the id of the start input element,
    the value of the start input element, the id of the stop input element, the value of the stop element
    the id of the div that holds the slider, the minimum allowed value, the maximum allowed value and the step size"""
    return range_template.substitute(start_id=start_id, start_value=start_value, stop_id=stop_id, 
        stop_value=stop_value, slider_id=slider_id, min_value=min_value, max_value=max_value, step=step)

def lightbox_init(selector="a[rel^='lightbox']", args=None):
    """create a lightbox for the current selector, you can also hand in
    args which is a dictionary of arguements, the default values are
    {"maxWidth":"'85%'", "maxHeight":"'85%'", "photo":"true"},
    you can look at other possible values at http://colorpowered.com/colorbox/ """
    defaults = {"maxWidth":"'85%'", "maxHeight":"'85%'", "photo":"true"}
    if args is not None:
        defaults.update(args)
    args = ','.join('%s:%s' % (key,value) for key,value in defaults.items())
    return lightbox_template.substitute(selector=selector, args=args)
    
def lightbox_init_youtube(selector="a[rel^='lightbox']", args=None):
    """create a lightbox customized for youtube
    the default values are {"iframe":"true", "onCleanup":"function(){ $('#colorbox iframe').attr('src', 'about:blank');", 
    "maxWidth":"'85%'", "maxHeight":"'85%'", "photo":"true"}
    you can look at other possible values at http://colorpowered.com/colorbox/ """
    defaults = {"iframe":"true", "onCleanup":"function(){ $('#colorbox iframe').attr('src', 'about:blank'); }"}
    if args is not None:
        defaults.update(args)
    return lightbox_init(selector=selector, args=defaults)
    
def lightbox_html():
    return ''

def nice_submit_button():
    "create the javascript for nice jquery submit buttons"
    return '$("input:submit").removeClass("submitChanges submit").button();'

def document_ready(seq):
    """create a javascript script tag for jquery document ready function which allows javascript to
    be run after the page has finished loading, it takes a sequence of javascript code to run
    all the init functions in this module are suitable to be used in this function"""
    return '<script type="text/javascript">$(document).ready(function(){' + '\n'.join(seq) +'});</script>'
    
def cycle_init(cycle_id, args=None):
    """create the javascript for a jquery cycler for the given cycle_id
    the default args are
    {'fx':"'fade'", 'speed':'300', 'timeout':'3000', 'pause':'1'}
    you can look at other possible values at http://jquery.malsup.com/cycle/
    """
    defaults = {'fx':"'fade'", 'speed':'300', 'timeout':'3000', 'pause':'1'}
    if args is not None:
        defaults.update(args)
    args = ','.join('%s:%s' % (key,value) for key,value in defaults.items())
    return cycle_template.substitute(cycle_id=cycle_id, args=args)

def cycle_html(cycle_id, seq):
    "create the html needs for the cycler code, it takes a sequence of html elements (divs, img, etc)"
    return '<div id="%s">%s</div>' % (cycle_id, ''.join(seq))
 
def cycle_html_youtube(cycle_id, lightbox_id, seq):
    """create the html for a youtube cycler, it needs to have a lightbox created and a cycler created
    it takes a sequence of (youtube ids, titles)"""
    sub = youtube_template.substitute
    seq = [sub(youtube_id=youtube_id, title=title, lightbox_id=lightbox_id, css_class='') for youtube_id, title in seq]
    return cycle_html(cycle_id, seq)

def carousel_init(carousel_id, args=None):
    """create the javascript for a carousel, you need to give a carousel_id
    you can also hand in optional arguements
    the default args are {'reflHeight':'56', 'reflGap':'2', 'mouseWheel':'true',
    'buttonLeft': '$("#left-button-[carousel_id]")', 'buttonRight':'$("#right-button-[carousel_id]")', 
    'altBox':'$("#alt-text-[carousel_id]")', 'titleBox':'$("#title-text-[carousel_id]")'}
    you can find arguements at http://www.professorcloud.com/mainsite/carousel.html
    """
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
    """this creates the carousel control ids for this id, you do not need to use this function
    normally"""
    return {'button_left':'left-button-%s' % carousel_id, 
        'button_right':'right-button-%s' % carousel_id, 
        'alt':'alt-text-%s' % carousel_id, 
        'title':'title-text-%s' % carousel_id}

def carousel_html(carousel_id, seq, args=None):
    """This creates the html for a carousel, it takes the id of the carousel
    and a seq of <a> around an image
    the default value is
    {'button_left':'<input id="%s" type="button" value="Left">', 
        'button_right':'<input id="%s" type="button" value="Right">', 
        'title':'<p id="%s"></p>', 
        'alt':'<p id="%s"></p>'}
    You can change those to any html objects that you want as long as you
    make sure that it has id="%s" in it so that right id can be put in
    """
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
    """This creates the html for a carousel setup for youtube
    you need to give it a carousel id and the id of the lightbox inside
    it takes a sequence of (youtube ids, titles)
    the defaults args are
    {'button_left':'<input id="%s" type="button" value="Left">', 
        'button_right':'<input id="%s" type="button" value="Right">', 
        'title':'<p id="%s"></p>', 
        'alt':'<p id="%s"></p>'}
    You can change those to any html objects that you want as long as you
    make sure that it has id="%s" in it so that right id can be put in    
    """
    sub = youtube_template.substitute
    seq = [sub(youtube_id=youtube_id, title=title, lightbox_id=lightbox_id, css_class='class="cloudcarousel"') for youtube_id, title in seq]
    return carousel_html(carousel_id, seq, args=None)