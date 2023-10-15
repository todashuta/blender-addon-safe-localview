# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Safe Localview",
    "author": "todashuta",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "-",
    "description": "-",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}


import bpy


class SafeLocalviewOperator(bpy.types.Operator):
    bl_idname = "view3d.safe_localview"
    bl_label = "Safe Localview"

    #frame_selected: bpy.props.BoolProperty(
    #        name="Frame Selected",
    #        description="Move the view to frame the selected objects",
    #        default=True)

    @classmethod
    def poll(cls, context):
        return bpy.ops.view3d.localview.poll()

    def execute(self, context):
        in_localview = context.space_data.local_view
        shading_type = context.space_data.shading.type
        if (in_localview and
                shading_type in {'MATERIAL', 'RENDERED'}):
            self.report({"INFO"}, "Viewport Shading changed to Wireframe")
            context.space_data.shading.type = 'WIREFRAME'

        frame_selected = context.preferences.addons[__name__].preferences.frame_selected

        return bpy.ops.view3d.localview(frame_selected=frame_selected)


class SafeLocalviewPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    frame_selected: bpy.props.BoolProperty(
            name="Frame Selected",
            description="Move the view to frame the selected objects",
            default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "frame_selected")


addon_keymaps = []


def register():
    bpy.utils.register_class(SafeLocalviewPreferences)
    bpy.utils.register_class(SafeLocalviewOperator)

    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(SafeLocalviewOperator.bl_idname, "SLASH", "PRESS")
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(SafeLocalviewOperator.bl_idname, "NUMPAD_SLASH", "PRESS")
    addon_keymaps.append((km, kmi))


def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(SafeLocalviewOperator)
    bpy.utils.unregister_class(SafeLocalviewPreferences)


if __name__ == "__main__":
    register()