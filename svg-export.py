try:
    import Rhino
    import scriptcontext
    import System
    GH=True
except:
    GH=False

'''This module is currently just a rough shot for sketching out ideas about svg
export.'''

def _s(o):
    if isinstance(o, str):
        if '_' in o:
            return o.replace('_','-')
        else: return o
    elif isinstance(o, System.Drawing.Color):
        return System.Drawing.ColorTranslator.ToHtml(att)
    else:
        return o

def xml_attributes(**kwargs):
    att_mask = '%s="%s"'
    return ' '.join([att_mask % (_s(k), kwargs[k]) for k in kwargs])

def to_svg(**kwargs):
    tag = kwargs.pop('tag')
    return '<%s %s />' % (tag, xml_attributes(**kwargs))

class svgRenderable(object):
    def render(self):
        if self.tag:
            return to_svg(**vars(self))
        else:
            print 'ERROR: no tag name'
            return

class svgCircle(svgRenderable):
    def __init__(self, cx, cy, r=4):
        self.tag = 'circle'
        self.cx = cx
        self.cy = cy
        self.r = r
        self.fill = 'black'

class svgPath(svgRenderable):
    def __init__(self, coords, color='#000', stroke='1px'):
        self.tag = 'path'
        self.fill = 'none'
        self.stroke = self.parse_color(color)
        self.stroke_width = self.parse_stroke(stroke)
        self.d = self.parse_coords(coords)
    def parse_coords(self, coords):
        coord_pairs = ['%s %s' % (c[0], c[1]) for c in coords]
        return 'M %s' % ' L '.join(coord_pairs)
    def parse_stroke(self, stroke):
        if isinstance(stroke, int) or isinstance(stroke, float):
            return '%spx' % stroke
        else: return stroke
    def parse_color(self, color):
        if isinstance(color, System.Drawing.Color):
            return System.Drawing.ColorTranslator.ToHtml(color)
        else: return color

def viewPoint(point3d, viewport):
    point2d = viewport.WorldToClient(point3d)
    return point2d.X, point2d.Y

def polylineToPath(viewport, polyline, color='#000', stroke='1px'):
    # get points from polyline
    pts = [pt for pt in polyline]
    # convert them to path coords
    coords = [viewPoint(p, viewport) for p in pts]
    path = svgPath(coords, color, stroke)
    return path.render()


def svg_wrap(*args):
    wrapper = '''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
%s
</svg>'''
    return wrapper % '\n'.join(args)

def html_wrap(svg, title='Grasshopper Export', css='', js=''):
    wrapper = '''
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>%s</title>
        <style type="text/css">
        %s
        </style>
    </head>
    <body>
        <div id="container">
        %s
        </div>
        <script type="text/javascript">
        </script>
    </body>
</html>'''
    return wrapper % (title, css, svg_wrap(*svg), js)

def parse_attribute_input(attributes):
    '''checks the incoming attribute inputs and converts
    them to dictionaries'''
    sample = attributes[0]
    if isinstance(sample, basestring):
        # deal with the string
        pass
    else:
        return attributes

def test():
    c1 = to_svg(tag='circle', r='10', cx=50, cy=20,
             stroke='#FF0000', fill='#0A0A0A')
    c = svgCircle(30, 70, 15)
    return svg_wrap(c1,c.render())

if GH:
    '''This part only runs if this code is pasted in a Grasshopper python
    component.
    Inputs
        export = A boolean switch to run the code (in case it's heavy)
        path = an optional file path to export to
        geometries = a geometry tree of stuff to turn into svg
        viewport = the view to export from (default is current viewport)
        attributes = optional list of key/value pairs to embed in the geometry
                        attributes can be python dictionaries
                        or they can be strings. One dictionary or string
                        is matched to one geometry.
    '''
    if points and fills and radii:
        circs = []
        for i, p in enumerate(points):
            c = svgCircle(p.X, p.Y, radii[i])
            color = fills[i]
            hex_color = System.Drawing.ColorTranslator.ToHtml(color)
            c.fill = hex_color
            circs.append(c)
        svgs = [n.render() for n in circs]
        a = svg_wrap(*svgs)
