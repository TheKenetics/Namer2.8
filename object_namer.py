bl_info = {
	"name": "Namer",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (2, 80, 0),
	"location": "View3D > Properties > Item",
	"description": "Adds the 'Item' menu back with a multiple object renaming feature.",
	"warning": "",
	"wiki_url": "",
	"category": "Object"
}

import bpy
from bpy.props import PointerProperty, StringProperty


class N_OT_multi_object_rename(bpy.types.Operator):
	"""Renames multiple objects with a common name"""
	bl_idname = "object.n_ot_multi_object_rename"
	bl_label = "Multi Object Rename"
	bl_options = {'REGISTER','UNDO'}

	# Properties
	name : StringProperty(
		name="Name",
		description="Name to use for objects"
	)

	@classmethod
	def poll(cls, context):
		return len(context.selected_objects) > 1

	def execute(self, context):
		for obj in context.selected_objects:
			obj.name = self.name
		
		return {'FINISHED'}


class N_OT_multi_object_add_prefix(bpy.types.Operator):
	"""Renames multiple objects with a prefix"""
	bl_idname = "object.n_ot_multi_object_add_prefix"
	bl_label = "Multi Object Add Prefix"
	bl_options = {'REGISTER','UNDO'}

	# Properties
	prefix : StringProperty(
		name="Prefix",
		description="Prefix to use for objects"
	)

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		for obj in context.selected_objects:
			obj.name = self.prefix + obj.name
		
		return {'FINISHED'}


class N_OT_multi_object_add_suffix(bpy.types.Operator):
	"""Renames multiple objects with a suffix"""
	bl_idname = "object.n_ot_multi_object_add_suffix"
	bl_label = "Multi Object Add Suffix"
	bl_options = {'REGISTER','UNDO'}

	# Properties
	suffix : StringProperty(
		name="Suffix",
		description="Suffix to use for objects"
	)

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		for obj in context.selected_objects:
			obj.name = obj.name + self.suffix
		
		return {'FINISHED'}


# Credit: Blender 2.79b
class N_PT_view3d_name(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Item"
	bl_label = "Item"

	@classmethod
	def poll(cls, context):
		return (context.space_data and context.active_object)

	def draw(self, context):
		layout = self.layout

		ob = context.active_object
		row = layout.row()
		row.label(text="", icon='OBJECT_DATA')
		row.prop(ob, "name", text="")

		if ob.type == 'ARMATURE' and ob.mode in {'EDIT', 'POSE'}:
			bone = context.active_bone
			if bone:
				row = layout.row()
				row.label(text="", icon='BONE_DATA')
				row.prop(bone, "name", text="")
		
		row = layout.row()
		row.prop(context.window_manager.n_runtime_settings , 'multi_name', text='')
		
		if len(context.selected_objects) > 1:
			row = layout.row()
			row.operator(N_OT_multi_object_rename.bl_idname).name = context.window_manager.n_runtime_settings.multi_name
		
		row = layout.row()
		row.operator(N_OT_multi_object_add_prefix.bl_idname).prefix = context.window_manager.n_runtime_settings.multi_name
		row = layout.row()
		row.operator(N_OT_multi_object_add_suffix.bl_idname).suffix = context.window_manager.n_runtime_settings.multi_name


class N_runtime_settings(bpy.types.PropertyGroup):
	multi_name : bpy.props.StringProperty(
		name="Multi Object Name",
		description="Name for Multiple Objects"
	)


def register():
	bpy.utils.register_class(N_runtime_settings)
	bpy.types.WindowManager.n_runtime_settings = PointerProperty(
		type=N_runtime_settings
		#name="Namer Runtime Settings"
	)
	
	bpy.utils.register_class(N_OT_multi_object_rename)
	bpy.utils.register_class(N_OT_multi_object_add_prefix)
	bpy.utils.register_class(N_OT_multi_object_add_suffix)
	bpy.utils.register_class(N_PT_view3d_name)


def unregister():
	bpy.utils.unregister_class(N_PT_view3d_name)
	bpy.utils.unregister_class(N_OT_multi_object_add_suffix)
	bpy.utils.unregister_class(N_OT_multi_object_add_prefix)
	bpy.utils.unregister_class(N_OT_multi_object_rename)
	
	del bpy.types.WindowManager.n_runtime_settings
	bpy.utils.unregister_class(N_runtime_settings)

if __name__ == "__main__":
	register()
