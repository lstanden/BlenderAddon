from bpy.types import Operator
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        IntProperty,
        StringProperty,
        FloatVectorProperty
        )
import bpy



class TERA_SHAPES_OT_add_aabb_collider(Operator):
    bl_idname = "tera.add_aabb_collider"
    bl_label = "Add AABB"
    bl_description = "Adds AABB to Shape"
    bl_options = {'REGISTER', 'UNDO'}

    label = StringProperty(name="label",
                           description="label that describes aabb collider")
    origin = FloatVectorProperty(name="origin",
                                 description="origin of collider",
                                 )

    extent = FloatVectorProperty(name="extent",
                                 description="extent of collider",
                                 )
    handler = None

    def draw_aabb(self, context):
        obj = util.getSelectedObjectShape()
        if (obj and self):
            l = obj.location
            origin = self.origin
            extent = self.extent
            draw_util.draw_wire_cube(
                l[0] + origin[0] - extent[0],
                l[0] + origin[0] + extent[0],
                l[1] + origin[1] - extent[1],
                l[1] + origin[1] + extent[1],
                l[2] + origin[2] - extent[2],
                l[2] + origin[2] + extent[2], (0, 0, 1, 1))

    def __init__(self):



    @classmethod
    def poll(cls, context):
        selected_object = util.getSelectedObjectShape()
        return (selected_object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.row().prop(self, "label")
        col.row().prop(self, "origin")
        col.row().prop(self, "extent")


    def execute(self, context):
        if(self.handler != None):
            bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
            self.handler = None
        if not self.label:
            self.report({"WARNING"},
                        "label for aabb required")
            return {'CANCELLED'}
        selected_object = util.getSelectedObjectShape()
        aabb = selected_object.tera_block.aabb.add()
        aabb.label = self.label
        aabb.origin = self.origin
        aabb.extent = self.extent
        return {'FINISHED'}


    def invoke(self, context, event):
        self.handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_aabb, (self, context), 'WINDOW', 'POST_VIEW')
        return context.window_manager.invoke_props_dialog(self, width = 400)


class TERA_SHAPES_OT_remove_aabb_collider(Operator):
    bl_idname = "tera.remove_aabb_collider"
    bl_label = "Remove AABB"
    bl_description = "Removes AABB"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        selected_object = util.getSelectedObjectShape()
        return (selected_object is not None)

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.row().prop(self, "aabb")

    def execute(self, context):
        selected_object = util.getSelectedObjectShape()
        selected_object.tera_block.aabb.remove(selected_object.tera_block.aabb_index)
        # aabb.label = self.label
        return {'FINISHED'}


    def invoke(self, context, event):
        return self.execute(context)
