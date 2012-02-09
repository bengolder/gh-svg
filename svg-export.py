try:
    import Rhino
    import scriptcontext
    import System
    GH=True
except:
    GH=False

'''This module is currently just a rough shot for sketching out ideas about svg
export.'''

def xml_attributes(**kwargs):
    att_mask = '%s="%s"'
    return ' '.join([att_mask % (k, kwargs[k]) for k in kwargs])

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
    def __init__(self, coords):
        self.tag = 'path'
        self.coords = coords


def svg_wrap(*args):
    wrapper = '''<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
%s
</svg>'''
    return wrapper % '\n'.join(args)


def test():
    c1 = to_svg(tag='circle', r='10', cx=50, cy=20,
             stroke='#FF0000', fill='#0A0A0A')
    c = svgCircle(30, 70, 15)
    return svg_wrap(c1,c.render())

if GH:
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



if __name__ == '__main__':
    f = open('test.svg', 'w')
    f.write(test())
    f.close()



