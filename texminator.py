import re
import bpy

bl_info = {
    "name": "Texminator",
    "blender": (2, 65, 0),
    "category": "Animation",
    'description': 'Texminator allows animating text',
    'author': 'Hanan Beer',
    'version': (1, 0),
    'blender': (2, 65, 0),
    'location': 'View3D',
    'category': 'Animation'
    #'warning': '', # used for warning icon and text in addons panel
    #'doc_url': '',
    #'tracker_url': '',
    #'support': '',
}


def is_curve(self, object):
    return object.type == 'FONT'

format_regex = r'\{(\w+)\}'
def on_frame(scene, depsgraph):
    text_obj = scene.texminators
    format_tmpl = scene.tex_format
    props = re.findall(format_regex, format_tmpl)
    items = { prop: text_obj.data.get(prop, '?') for prop in props }
    text_obj.data.body = format_tmpl.format(**items)

class TexminatorPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport N Panel"""
    bl_label = "Texminator"
    bl_idname = "OBJECT_PT_texminator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texminator"

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene, "texminators", text="Text")
        layout.prop(bpy.context.scene, "tex_format", text="Format")
    
def register():

    bpy.types.Scene.texminators = bpy.props.PointerProperty(type=bpy.types.Object, poll=is_curve)
    bpy.types.Scene.tex_format = bpy.props.StringProperty()
    bpy.utils.register_class(TexminatorPanel)

def unregister():
    bpy.app.handlers.frame_change_post.clear()
    bpy.utils.unregister_class(TexminatorPanel)


register()
