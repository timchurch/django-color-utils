django-color-utils
===================

Collection of color picker widgets and color database model fields for Django.


Color Picker Form Widgets
=======
These color pickers are all open-source and freely available online.  All credit goes to the original authors.  I have simply adapted each one to be used as a Django form widget.

* [Bootstrap Color Picker](http://www.eyecon.ro/bootstrap-colorpicker/) by [Stephan Petre](http://www.eyecon.ro/)
* [Colorwheel](http://jweir.github.com/colorwheel/) by [John Weir](http://famedriver.com/)
* [Farbtastic](http://acko.net/blog/farbtastic-jquery-color-picker-plug-in/) by [Steven Wittens](http://acko.net/)
* [Flexi Color Picker](http://www.daviddurman.com/flexi-color-picker/) by [David Durman](http://www.daviddurman.com/)
* HTML5 Color Input - input[type='color']
* [jPicker](http://www.digitalmagicpro.com/jPicker/) by [Digital Magic Pro](http://www.digitalmagicpro.com/)
* [JSColor](http://jscolor.com) by Jan Odvárko
* [MenuCool Color Picker](http://www.menucool.com/color-picker)
* [MooRainbow](http://moorainbow.woolly-sheep.net/) by Djamil Legato
* [Photoshop-style Color Picker](http://www.eyecon.ro/colorpicker/) by [Stephan Petre](http://www.eyecon.ro/)
* [Really Simple Color Picker](http://laktek.com/2008/10/27/really-simple-color-picker-in-jquery/) by [Lakshan Perera](http://laktek.com/about)
* [SimpleColor](http://recursive-design.com/projects/jquery-simple-color/) by [Dave Perrett](http://recursive-design.com/)
* [Spectrum](http://bgrins.github.com/spectrum/) by Brian Grinstead


Fields
======
Django model fields for storing color values in different formats including hex, RGB, RGBA, HSL, and HSV.

TODO


Usage
======

* 1. Add 'color_utils' to your installed apps:

```python
INSTALLED_APPS = (
  ...

  'color_utils',

  ...
)
```

* 2. In your forms.py file override form widgets with widgets from color_utils. For example if using model forms:

```python
from django.forms import ModelForm
from . import models

from color_utils import widgets as color_widgets

class MyColorfulModelForm(ModelForm):
    class Meta:
        model = models.MyColorfulModel
        widgets = {
            'my_color_field': color_widgets.HTML5ColorInput(),
        }
```
