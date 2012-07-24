from django import forms
from django.forms import widgets
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from color_utils.utils import hex_to_rgb


try:
    STATIC_URL_BASE = settings.STATIC_URL
except AttributeError:
    try:
        STATIC_URL_BASE = settings.MEDIA_URL
    except AttributeError:
        STATIC_URL_BASE = ''


class HTML5ColorInput(widgets.Input):
    """
    HTML 5 color input (Currently only supported by Chrome and Opera)
    Uses the browsers default color input interface
    Only supports 6 digit Hex value (as per W3C spec)
    TODO: specify fallback widget?
    """
    input_type = 'color'


class ReallySimpleColorPicker(forms.TextInput):
    """
    Based on http://laktek.com/2008/10/27/really-simple-color-picker-in-jquery/
    Requires jQuery > 1.2.6
    
    Displays a fixed set of preselected color options.  Hex value can also be edited manually.
    Only supports Hex values.  Alpha channel not supported.
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/really-simple/colorPicker.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/really-simple/jquery.colorPicker.js',)

    def render(self, name, value, attrs=None):
        rendered = super(ReallySimpleColorPicker, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').colorPicker();
            </script>''' % name)


class BootstrapColorPicker(forms.TextInput):
    """
    Based on Stefan Petre's bootstrap color picker - http://www.eyecon.ro/bootstrap-colorpicker/
    
    A color picker that is designed to integrate with the Twitter Bootstrap CSS framework.
    Supports Hex, RGB, RGBA, HSV, and HSVA
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/bootstrap/css/bootstrap.min.css',
                       STATIC_URL_BASE + 'color_utils/bootstrap/css/colorpicker.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/bootstrap/js/bootstrap-colorpicker.js',)

#    def _render_js(self, _id):
#        js = u"""
#        <script type="text/javascript">
#            $(document).ready(function(){
#                $('#%s').colorpicker({
#                    format: 'hex'
#                });
#            });
#        </script>
#            """ % _id
#        return js
#
#    def _render_html_addon(self, name, value, attrs=None):
##        _format = "hex"  # TODO: how to allow alternate formats (rgb, rgba, hsb)
#        rendered_input = super(BootstrapColorPicker, self).render(name, value, attrs)
#        html = """
#            <div class="input-append color" data-color="%s">
#              %s
#              <span class="add-on"><i style="background-color:#%s"></i></span>
#            </div>
#        """ % (value, rendered_input, value)
#        return html
#
#    def _render_html_basic(self, name, value, attrs=None):
#        return super(BootstrapColorPicker, self).render(name, value, attrs)
#
#    def render(self, name, value, attrs=None):
#        if not 'id' in attrs:
#            attrs['id'] = "id_%s" % name
#        return mark_safe(self._render_html_basic(name, value, attrs) + self._render_js(attrs['id']))
    
    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        rendered_input = super(BootstrapColorPicker, self).render(name, value, attrs)
        return render_to_string('color_utils/bootstrap-append.html', locals())


class PhotoshopColorPicker(forms.TextInput):
    """
    Based on Stefan Petre's Photoshop-style color picker - http://www.eyecon.ro/colorpicker/
    Inspired by django-colors - http://code.google.com/p/django-colors/
    
    Supports 
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/photoshop/css/colorpicker.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/photoshop/js/colorpicker.js',)

    def _render_js(self, _id, value):
        js = u"""
<script type="text/javascript">
$(document).ready(function(){
    var preview = $('<div class="color-picker-preview"><div style="background-color:#%s"></div></div>').insertAfter('#%s');
    $('#%s').ColorPicker({
        color: '%s',
        onSubmit: function(hsb, hex, rgb, el) { $(el).val(hex); $(el).ColorPickerHide();$(preview).find('div').css('backgroundColor', '#' + hex); },
        onBeforeShow: function () { $(this).ColorPickerSetColor(this.value); }
    }).bind('keyup', function(){ $(this).ColorPickerSetColor(this.value); });
});
</script>""" % (value, _id, _id, value)
        return js

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        rendered = super(PhotoshopColorPicker, self).render(name, value, attrs)
        return mark_safe(rendered + self._render_js(attrs['id'], value))


class ColorWheelColorPicker(forms.TextInput):
    """
    Based on John Weir's color wheel - http://jweir.github.com/colorwheel/
    """
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/colorwheel/raphael-min.js',
              STATIC_URL_BASE + 'color_utils/colorwheel/colorwheel.js',)

    # TODO: add width option
    def _render_js(self, colorwheel_id, input_id, value):
        js = u"""
<script type="text/javascript">
    $(document).ready(function(){
        var cw = Raphael.colorwheel($("#%s")[0],120);
        cw.input($("#%s")[0]).color("%s");
    });
</script>""" % (colorwheel_id, input_id, value)
        return js

    def _render_html(self, name, value, attrs=None):
#        _format = "hex"  # TODO: how to determine this?
        rendered_input = super(ColorWheelColorPicker, self).render(name, value, attrs)
        colorwheel_id = attrs['id'] + "-colorwheel"
        html = """
            <div class="colorwheel-container">
              %s
              <div id="%s" class="colorwheel"></div>
            </div>
        """ % (rendered_input, colorwheel_id)
        return html

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
#        rendered = super(ColorWheelColorPicker, self).render(name, value, attrs)
        return mark_safe(self._render_html(name, value, attrs) + 
                         self._render_js(attrs['id'] + '-colorwheel', attrs['id'], value))


class JSColorColorPicker(forms.TextInput):
    """
    Based on JSColor - http://jscolor.com
    Note:  Requires input to use class 'color'
    """
    class Media:
        js = (STATIC_URL_BASE + 'color_utils/jscolor/jscolor.js',)

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name

        if 'class' in attrs:
            attrs['class'] = attrs['class'] + ' color'
        else:
            attrs['class'] = 'color'

        return super(JSColorColorPicker, self).render(name, value, attrs)


class SimpleColorPicker(forms.TextInput):
    """
    Based on Recursive Design's jQuery SimpleColor Plugin - http://recursive-design.com/projects/jquery-simple-color/
    """
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/simplecolor/jquery.simple-color.min.js',)

    def _render_js(self, _id, value):
        js = u"""
<script type="text/javascript">
    $(document).ready(function(){
        $('#%s').simpleColor();
    });
</script>""" % _id
        return js

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        rendered = super(SimpleColorPicker, self).render(name, value, attrs)
        return mark_safe(rendered + self._render_js(attrs['id'], value))


class SpectrumColorPicker(forms.TextInput):
    """
    Based on Brian Grinstead's Spectrum - http://bgrins.github.com/spectrum/
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/spectrum/spectrum.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/spectrum/spectrum.js',)

    def _render_js(self, _id, value):
        js = u"""
<script type="text/javascript">
    $(document).ready(function(){
        $('#%s').spectrum({
            color: "#%s"
        });
    });
</script>""" % (_id, value)
        return js

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        rendered = super(SpectrumColorPicker, self).render(name, value, attrs)
        return mark_safe(rendered + self._render_js(attrs['id'], value))


class FarbtasticColorPicker(forms.TextInput):
    """
    Based on http://acko.net/blog/farbtastic-jquery-color-picker-plug-in/
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/farbtastic/farbtastic.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/farbtastic/farbtastic.js',)

    def _get_colorpicker_id(self, input_id):
        """Returns the HTML id for the colorpicker"""
        return "%s-colorpicker" % input_id

    def _render_js(self, input_id, value):
        js = u"""
<script type="text/javascript">
    $(document).ready(function(){
        $('#%s').farbtastic('#%s');
    });
</script>""" % (self._get_colorpicker_id(input_id), input_id)
        return js

    def _render_html(self, name, value, attrs=None):
        rendered_input = super(FarbtasticColorPicker, self).render(name, value, attrs)
        colorpicker_id = self._get_colorpicker_id(attrs['id'])
        html = """
            %s
            <div id="%s" class="farbtastic"></div>
        """ % (rendered_input, colorpicker_id)
        return html

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        return mark_safe(self._render_html(name, value, attrs) +
                         self._render_js(attrs['id'], value))


#class ColrdClassicColorPicker(forms.TextInput):
#    """
#    Based on http://colrd.com/misc/labs/Color-Picker/Classic/index.html
#    """
#    pass
#
#
#class ColrdAdvancedColorPicker(forms.TextInput):
#    """
#    Based on http://colrd.com/misc/labs/Color-Picker/HSL+RGBA/index.html
#    """
#    pass


#class ColrdMiniSphereColorPicker(forms.TextInput):
#    """
#    Based on http://colrd.com/misc/labs/Color-Picker/Mini-Sphere/index.html
#    """
#    class Media:
#        js = [STATIC_URL_BASE + 'color_utils/farbtastic/farbtastic.js',]
#    
#    def _render_js(self, input_id, value):
#        js = u"""
#<script type="text/javascript">
#    
#</script>""" % (self._get_colorpicker_id(input_id), input_id)
#        return js
#
#    def _render_html(self, name, value, attrs=None):
#        rendered_input = super(FarbtasticColorPicker, self).render(name, value, attrs)
#        colorpicker_id = self._get_colorpicker_id(attrs['id'])
#        html = """
#<div id="mini" onmousedown="Picker.core('mini',event); return false;" onselectstart="return false;">
#    <div class="north"><span id="mHEX">FFFFFF</span></div>
#    <div class="south" id="mSpec" style="HEIGHT: 128px; WIDTH: 128px;" onmousedown="Picker.core('mCur',event)">
#        <div id="mCur" style="TOP: 86px; LEFT: 68px;"></div>
#        <img src="./media/circle.png" onmousedown="return false;" ondrag="return false;" onselectstart="return false;">
#        <img src="./media/resize.gif" id="mSize" onmousedown="Picker.core('mSize',event); return false;" ondrag="return false;" onselectstart="return false;">
#    </div>
#</div>
#""" 
#        
#        """
#            %s
#            <div id="%s" class="farbtastic"></div>
#        """ % (rendered_input, colorpicker_id)
#        return html
#
#    def render(self, name, value, attrs=None):
#        if not 'id' in attrs:
#            attrs['id'] = "id_%s" % name
#        return mark_safe(self._render_html(name, value, attrs) +
#                         self._render_js(attrs['id'], value))


class jPickerColorPicker(forms.TextInput):
    """
    Based on http://www.digitalmagicpro.com/jPicker/
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/jpicker/css/jpicker-1.1.6.min.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/jpicker/jpicker-1.1.6.min.js',)

    def _render_js(self, _id, value):
        js = u"""
<script type="text/javascript">
    $(document).ready(function(){
        $('#%s').jPicker({
            images: {
                clientPath: '%scolor_utils/jpicker/images/'
            }
        });
    });
</script>""" % (_id, STATIC_URL_BASE)
        return js

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        rendered = super(jPickerColorPicker, self).render(name, value, attrs)
        return mark_safe(rendered + self._render_js(attrs['id'], value))


class FlexiColorPicker(forms.TextInput):
    """
    Based on http://www.daviddurman.com/flexi-color-picker/
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/flexi/themes.css',)}
        js = ('//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js',
              STATIC_URL_BASE + 'color_utils/flexi/colorpicker.js',)

    def _render_js(self, input_id, name, value):
        js = u"""
<script type="text/javascript">
    ColorPicker(
        document.getElementById('%s-slide'),
        document.getElementById('%s-picker'),
        function(hex, hsv, rgb) {
            input = document.getElementById('%s');
            input.value = hex;
            input.style.backgroundColor = hex;
        });
</script>""" % (name, name, input_id)
        return js

    def _render_html(self, name, value, attrs=None):
        rendered_input = super(FlexiColorPicker, self).render(name, value, attrs)
        picker_id = name + '-picker'
        slide_id = name + '-slide'
        html = """
            %s
            <div id="color-picker" class="cp-default">
                <div id="%s" class="picker-wrapper"></div>
                <div id="%s" class="slide-wrapper"></div>
            </div>
        """ % (rendered_input, picker_id, slide_id)
        return html

    def _render_css(self, name):
        """
        This is a hack.
        No default style is given so this is a temporary default setting...
        """
        css = """
<style type="text/css">
    #%s-picker { width: 200px; height: 200px }
    #%s-slide { width: 30px; height: 200px }
</style>""" % (name, name)
        return css

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        return mark_safe(self._render_html(name, value, attrs) +
                         self._render_js(attrs['id'], name, value) + 
                         self._render_css(name))


class MooRainbowColorPicker(forms.TextInput):
    """
    Based on http://moorainbow.woolly-sheep.net/
    Requires MooTools v1.11
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/moorainbow/mooRainbow.css',)}
        js = (STATIC_URL_BASE + 'color_utils/moorainbow/mootools.v1.11.js',
              STATIC_URL_BASE + 'color_utils/moorainbow/mooRainbow.js',)
#        # Note: doesn't seem to work with mootools > 1.11
#        js = (STATIC_URL_BASE + 'color_utils/moorainbow/mootools-core-1.4.5-full-compat-yc.js',
#              STATIC_URL_BASE + 'color_utils/moorainbow/mootools-more-1.4.0.1.js',  # required for Drag
#              STATIC_URL_BASE + 'color_utils/moorainbow/mooRainbow.1.2b2.js',)

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name

        STATIC_URL = STATIC_URL_BASE
        rgb = hex_to_rgb(value)
        rendered_input = super(MooRainbowColorPicker, self).render(name, value, attrs)

        return render_to_string('color_utils/moorainbow.html', locals())


class MenuCoolColorPicker(forms.TextInput):
    """
    Based on http://www.menucool.com/color-picker
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'color_utils/menucool/mcColorPicker.css',)}
        js = (STATIC_URL_BASE + 'color_utils/menucool/mcColorPicker.js',)

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name

        # Input required to have class 'color'
        if 'class' in attrs:
            attrs['class'] = attrs['class'] + ' color'
        else:
            attrs['class'] = 'color'

        rendered_input = super(MenuCoolColorPicker, self).render(name, value, attrs)

        return render_to_string('color_utils/menucool.html', locals())
