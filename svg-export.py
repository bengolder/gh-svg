try:
    import Rhino
    import scriptcontext
    import System
    GH=True
except:
    GH=False

'''This module is currently just a rough shot for sketching out ideas about svg
export.'''


FEATURE_TRANSLATOR = (
        'Point', 'Point3d'
        'MultiPoint', 'Point3d'
        'LineString', 'Curve', 'Polyline'
        'MultiLineString','Curve', 'Polyline'
        'Polygon',
        'MultiPolygon',
        )

def conversion_lookup(g):
    if isinstance(g, Rhino.Geometry.Point3d):
        return to_svg_point
    elif isinstance(g, Rhino.Geometry.Polyline):
        return to_svg_polyline
    elif isinstance(g, Rhino.Geometry.Curve):
        return to_svg_curve
    else:
        try:
            to_svg_curve
        except:
            print 'This geometry could not be converted:'
            print type(g)
            raise

def to_svg_point(vp, g, atts):
    x, y = viewPoint(g, vp)
    return svgCircle(x,y)

def to_svg_polyline(vp, g, atts):
    polyline = g.TryGetPolyline()[1]
    # get points from polyline
    pts = [pt for pt in polyline]
    # convert them to path coords
    coords = [viewPoint(p, vp) for p in pts]
    return svgPolyline(coords, atts)

def to_svg_curve(vp, g, atts):
    poly = g.ToPolyline(0,0,0.01, 0.1, tol, 0, 0, True, g.Domain)
    return to_svg_polyline(vp, poly, atts)

def viewPoint(point3d, viewport):
    point2d = viewport.WorldToClient(point3d)
    return point2d.X, point2d.Y


def xml_attributes(**kwargs):
    att_mask = '%s="%s"'
    atts = []
    for key in ('id', 'class'):
        if key in kwargs:
            atts.append((key, kwargs.pop(key)))
    for k in kwargs:
        atts.append((k, kwargs[k]))
    return ' '.join([att_mask % a for a in atts])

def to_svg(**kwargs):
    tag = kwargs.pop('tag')
    return '<%s %s />' % (tag, xml_attributes(**kwargs))

class svgRenderable(object):
    def render(self):
        if self.tag:
            d = vars(self)
            # blend attributes into dictionary
            d.update(d.pop('attributes'))
            return to_svg(**d)
        else:
            print 'ERROR: no tag name'
            return

class svgCircle(svgRenderable):
    def __init__(self, cx, cy, attributes):
        self.tag = 'circle'
        self.cx = cx
        self.cy = cy
        self.attributes = attributes

class svgPolyline(svgRenderable):
    def __init__(self, coords, attributes):
        self.tag = 'path'
        self.d = self.parse_coords(coords)
        self.attributes = attributes
    def parse_coords(self, coords):
        coord_pairs = ['%s %s' % (c[0], c[1]) for c in coords]
        return 'M %s' % ' L '.join(coord_pairs)

def svg_wrap(svgs):
    wrapper = '''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
%s
</svg>'''
    return wrapper % '\n'.join(svgs)

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
        %s
        </script>
    </body>
</html>'''
    return wrapper % (title, css, svg_wrap(svg), js)

def build_svg_text(geometry, atts, viewport):
    out = []
    for i, g in enumerate(geometry):
        svg = conversion_lookup(g)(viewport, g, atts[i])
        txt = svg.render()
        out.append(txt)
    return out

if GH:
    '''This part only runs if this code is pasted in a Grasshopper python
    component.
    '''
    if geometry and create_svg:
        # run the script
        if attribute_dictionaries:
            # unwrap the attribute dictionaries, just get their normal
            # dictionaries
            atts = [a.d for a in attribute_dictionaries]
        else:
            atts = []
        if not viewport:
            viewport = scriptcontext.doc.Views.ActiveView.ActiveViewport
        tol = polyline_tol
        svg_text = html_wrap(build_svg_text(geometry, atts, viewport), title, css, js)
