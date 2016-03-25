#gh-svg

---

Note: This code is no longer under active development. See below for more details.

__gh-svg__ is a plugin for exporting [svg](http://www.w3.org/Graphics/SVG/) data from the [Grasshopper](http://grasshopper3d.com) and
[Rhino](http://www.rhino3d.com/) 3D modeling environments. The intent is work towards create greater
interoperability between different geometry editing softwares using open-source data
format standards, as well as making it easier to create dynamic interfaces
for topics that rely heavily on illustration and geometry, such as architecture,
urban design, industrial design, and data visualization.


Here's an [example](http://benjamingolder.com/static/files/dynamic_example.html).
And another [example](http://benjamingolder.com/static/files/bcn_example.html).


## The Current State of this Software

_March 26, 2016 ---_ I haven't worked on this code for years. This project has been abandoned. It was a neat experiment, but was a clunky implementation and is likely obselete today. Others have written better implementations. For example, [the decodes library](http://decod.es/) includes [an svg io module](https://github.com/ksteinfe/decodes/blob/master/decodes/io/svg_out.py). 

_March 7th, 2012 ---_ The export now supports arbitrary attributes, giving priority to ids and classes. I tested the attributes to see how well they
could handle unicode text, just to be sure it wasn't creating another little ascii unicode death trap.
I created a component for inputting css,
javascript, and wrapping everything in html. I'm still not sure how NURBS
curves should be handled, but for now it will default to approximating them
with polylines to an input tolerance (which seems to work pretty well for
illustration purposes). The whole thing runs pretty slow. It seemed to break
down when writing only about 884 moderately complex polylines.

_February 27th, 2012 ---_ I've now created some simple Dot and Polyline export
examples. They are a little slow, but they work fine.

_February 5th, 2012 ---_ I just made this repository for the project, and expect to
develop the plugin over the next several months. If you are interested in this
project, please 'watch' it here on Github.


## Next Steps to Development

* Point/Dot Export (Done!)
* Polylines Export (Done!)
* Viewport Projection (Done!)
* Embedding arbitrary attributes (Done!)
* Viewport Selection (ok, soon)
* Curve Export (no beziers yet, but polyline approximation works)

## But why?

Here’s why I think SVG is a good file format to export to:

1. SVG can be read by any common browser, and therefore there is no need for special software to view it.
2. SVG can be easily read and edited by most vector editing software, including Adobe Illustrator and many open source softwares.
style information can be easily embedded in the geometry, or can be adjusted with a style sheet
3. SVG is dynamic. This means I can create geometry with Rhino with embedded hypertext links, or I can use Javascript to display information when someone hovers their mouse over the geometry.

