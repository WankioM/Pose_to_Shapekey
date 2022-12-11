import bpy

bl_info = {
    "name": "Pose to Shape Key",
    "author": "Tracy Wankio",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Changes poses to keyframes",
    "warning": "Frames under 100",
    "doc_url": "https://github.com/WankioM/Pose_to_Shapekey/blob/main/README.md",
    "category": "",
}



def create_shape_keys(frames):
    C = bpy.context
    for i in range(1, frames):
        
        #Reference frame number
        C.scene.frame_current = i      
        
        #Apply shape key
        C.area.type ="PROPERTIES"
        C.space_data.context = 'MODIFIER' 
        bpy.ops.object.modifier_set_active(modifier="Armature")
        print("chosen modif key")
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="Armature")
        



def keyframing(frames):
    C = bpy.context
    C.area.type ="PROPERTIES"
    C.space_data.context = 'DATA'
        
    for i in range(1, frames):
        C.scene.frame_current = i

        #Keyframe shape keys
       
        bpy.context.object.active_shape_key_index = i
        if i <10:
            bpy.data.shape_keys["Key"].key_blocks[f"Armature.00{i}"].value = 1   
            bpy.context.object.data.shape_keys.key_blocks[f"Armature.00{i}"].keyframe_insert(data_path='value', frame=i)
           
        elif i >=10:
            bpy.data.shape_keys["Key"].key_blocks[f"Armature.0{i}"].value = 1   
            bpy.context.object.data.shape_keys.key_blocks[f"Armature.0{i}"].keyframe_insert(data_path='value', frame=i)
        
        #Change frame to next and set value back to 0
        C.scene.frame_current = i+1
        bpy.context.object.active_shape_key_index = i
        
        if i <10:
            bpy.data.shape_keys["Key"].key_blocks[f"Armature.00{i}"].value = 0
            bpy.context.object.data.shape_keys.key_blocks[f"Armature.00{i}"].keyframe_insert(data_path='value', frame=i+1) 
        
            #previous frame to 0
            bpy.context.object.data.shape_keys.key_blocks[f"Armature.00{i}"].keyframe_insert(data_path='value', frame=i-1)  
            
        if i>=10:
            bpy.data.shape_keys["Key"].key_blocks[f"Armature.0{i}"].value = 0
            bpy.context.object.data.shape_keys.key_blocks[f"Armature.0{i}"].keyframe_insert(data_path='value', frame=i+1) 
        
            #previous frame to 0
            bpy.context.object.data.shape_keys.key_blocks[f"Armature.0{i}"].keyframe_insert(data_path='value', frame=i-1) 
        


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Pose_to_Shape"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= "Pose to Shape Key"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("wm.textop", text='Generate Shape Keys', icon='GHOST_ENABLED')
        row = layout.row()
        row.operator("wm.animop", text='Animate Shape Keys', icon='KEYFRAME_HLT')
        row = layout.row()
        row.operator("wm.delop", text='Delete Shape Keys', icon='REMOVE')
        
#Dialog box
        
class WM_OT_textOp(bpy.types.Operator):
    bl_label = "Generate_ShapeKeys"
    bl_idname = "wm.textop"
    
    frame_num:bpy.props.IntProperty(name='Enter Number of Frames:', default=0)
    
   
    def execute(self, context):
        frames=self.frame_num
        create_shape_keys(frames)
        bpy.context.area.type ="VIEW_3D"
        
        return {'FINISHED'}
    
    def invoke (self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class WM_OT_animOp(bpy.types.Operator):
    bl_label = "Animate Shape Keys"
    bl_idname = "wm.animop"
    
    frame_num:bpy.props.IntProperty(name='Enter Number of frames:', default=0)
   
    def execute(self, context):
        frames=self.frame_num
        keyframing(frames)
        bpy.context.area.type ="VIEW_3D"
        
        return {'FINISHED'}
    
    def invoke (self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class WM_OT_delOp(bpy.types.Operator):
    bl_label = "Delete all Shape Keys"
    bl_idname = "wm.delop"
    

   
    def execute(self, context):
        bpy.ops.object.shape_key_remove(all=True)
        
        return {'FINISHED'}
    
    def invoke (self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    
    

def register():
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(WM_OT_textOp)
    bpy.utils.register_class(WM_OT_animOp)
    bpy.utils.register_class(WM_OT_delOp)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(WM_OT_textOp)
    bpy.utils.unregister_class(WM_OT_animOp)
    bpy.utils.unregister_class(WM_OT_delOp)


if __name__ == "__main__":
    register()



