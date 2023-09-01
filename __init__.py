bl_info = {
    "name": "Configure Custom Properties Panel",
    "author":"Estudio 3D UNSL-TV",
    "version":(2, 4, 8),
    "blender": (3, 5, 0),
    "location": "View3D > N Panel > Controlador de Propiedades",
    "description": "Permite controlar todas las Custom Properties situadas en los huesos c_pos desde un mismo lugar",
    "category": "3D View",
}

import bpy

from . import addon_updater_ops

class RenderSettingsB(bpy.types.Panel):
    bl_label = "Render Settings Presets"
    bl_idname = "OBJECT_PT_viewport_render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.operator('object.vr_operator')
        box.operator('object.lr_operator')
        box.operator('object.fr_operator')
 
class VRSettingsOp(bpy.types.Operator):
    bl_label = "Viewport Animación"
    bl_description = "Configura la Escena para Renderizar bajo cierto preset"
    bl_idname = 'object.vr_operator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"
    
    def execute(self, context):
        # Simplify Viewport Config
        bpy.context.scene.render.use_simplify = True
        bpy.context.scene.render.simplify_subdivision = 0
        bpy.context.scene.render.simplify_child_particles = 0
        bpy.context.scene.render.simplify_volumes = 0
        bpy.context.scene.render.simplify_shadows = 0
                
        # Simplify Render Config
        bpy.context.scene.render.simplify_subdivision_render = 1
        bpy.context.scene.render.simplify_shadows_render = 0.1
    
        # Curves Config
        bpy.context.scene.render.hair_type = 'STRIP'
        bpy.context.scene.render.hair_subdiv = 0
        
        # DOF Config
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
        bpy.context.scene.eevee.use_bokeh_jittered = True
        bpy.context.scene.eevee.bokeh_overblur = 20
                
        # SSR Config
        bpy.context.scene.eevee.use_ssr = True
        bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_ssr_halfres = True
        bpy.context.scene.eevee.ssr_quality = 0
        bpy.context.scene.eevee.ssr_max_roughness = 1
        
        # Motion Blur Config
        bpy.context.scene.eevee.use_motion_blur = False

        # Shadows Config
        bpy.context.scene.eevee.shadow_cube_size = '128'
        bpy.context.scene.eevee.shadow_cascade_size = '256'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True
        bpy.context.scene.eevee.use_soft_shadows = True
        
        # Volumetrics Config
        bpy.context.scene.eevee.volumetric_tile_size = '16'
        bpy.context.scene.eevee.volumetric_samples = 32
        
        # Metadata Config
        bpy.context.scene.render.use_stamp_date = True
        bpy.context.scene.render.use_stamp_time = False
        bpy.context.scene.render.use_stamp_render_time = False
        bpy.context.scene.render.use_stamp_frame = True
        bpy.context.scene.render.use_stamp_frame_range = False
        bpy.context.scene.render.use_stamp_memory = False
        bpy.context.scene.render.use_stamp_hostname = False
        bpy.context.scene.render.use_stamp_camera = True
        bpy.context.scene.render.use_stamp_lens = True
        bpy.context.scene.render.use_stamp_scene = False
        bpy.context.scene.render.use_stamp_marker = False
        bpy.context.scene.render.use_stamp_filename = True
        bpy.context.scene.render.use_stamp_sequencer_strip = False
        
        # Stamp Config
        bpy.context.scene.render.use_stamp = True
        bpy.context.scene.render.stamp_font_size = 24

        # Render Config
        bpy.context.scene.eevee.taa_render_samples = 8
        bpy.context.scene.eevee.taa_samples = 8       
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        
        # Output Config
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'NONE'
        bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
        bpy.context.scene.render.ffmpeg.gopsize = 25
        bpy.context.scene.render.ffmpeg.video_bitrate = 12000
        bpy.context.scene.render.ffmpeg.minrate = 12000
        bpy.context.scene.render.ffmpeg.maxrate = 12000
        bpy.context.scene.render.ffmpeg.buffersize = 2000
        
        bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'
        bpy.context.scene.render.ffmpeg.audio_channels = 'STEREO'
        
        # CP Config
        bone_name = "c_pos"
        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                keys_list = list(c_pos_bone.keys())
                for vrprop in keys_list:
                    if vrprop not in ['_RNA_UI']:
                        if vrprop.startswith("001-CantidadPelo"):
                            if "_RNA_UI" not in c_pos_bone:
                                c_pos_bone["_RNA_UI"] = {}
                            if "001-CantidadPelo" not in c_pos_bone["_RNA_UI"]:
                                c_pos_bone["_RNA_UI"]["001-CantidadPelo"] = {}
                            c_pos_bone["_RNA_UI"]["001-CantidadPelo"]["min"] = 0.0
                            c_pos_bone["_RNA_UI"]["001-CantidadPelo"]["max"] = 1.0
                            c_pos_bone[vrprop] = 0.0
                            obj.update_tag(refresh={'OBJECT'})
        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                for vrpropcm in c_pos_bone.keys():
                    if vrpropcm not in ['_RNA_UI']:
                        if vrpropcm.startswith("002-CorneaMask"):
                            c_pos_bone[vrpropcm] = 0
                            obj.update_tag(refresh={'OBJECT'})
        bpy.context.view_layer.update()

        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                for vrpropvm in c_pos_bone.keys():
                    if vrpropvm not in ['_RNA_UI']:
                        if vrpropvm.startswith("VisorMask"):
                            c_pos_bone[vrpropvm] = 0
                            obj.update_tag(refresh={'OBJECT'})
        bpy.context.view_layer.update()

        for obj in bpy.data.objects:
            name = obj.name.lower().replace("ó", "o")
            if name == "vegetacion":
                obj.hide_viewport = True
            if obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION' and obj.instance_collection:
                instance_name = obj.instance_collection.name.lower().replace("ó", "o")
                if instance_name == "vegetacion":
                    obj.hide_viewport = True
        for collection in bpy.data.collections:
            name = collection.name.lower().replace("ó", "o")
            if name == "vegetacion":
                collection.hide_viewport = True
        bpy.context.view_layer.update()
        
        return {'FINISHED'}
    
class LRSettingsOp(bpy.types.Operator):
    bl_label = "Render Previo"
    bl_description = "Configura la Escena para Renderizar bajo cierto preset"
    bl_idname = 'object.lr_operator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"
    
    def execute(self, context):
        # Simplify Viewport config
        bpy.context.scene.render.use_simplify = True
        bpy.context.scene.render.simplify_subdivision = 1
        bpy.context.scene.render.simplify_child_particles = 1
        bpy.context.scene.render.simplify_volumes = 1
        bpy.context.scene.render.simplify_shadows = 1
        
        # Simplify Render Config
        bpy.context.scene.render.simplify_subdivision_render = 1
        bpy.context.scene.render.simplify_shadows_render = 0.1
    
        # Curves Config
        bpy.context.scene.render.hair_type = 'STRIP'
        bpy.context.scene.render.hair_subdiv = 1
        
        # DOF Config
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
        bpy.context.scene.eevee.use_bokeh_jittered = True
        bpy.context.scene.eevee.bokeh_overblur = 20
        
        # SSR Config
        bpy.context.scene.eevee.use_ssr = True
        bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_ssr_halfres = True
        bpy.context.scene.eevee.ssr_quality = 0
        bpy.context.scene.eevee.ssr_max_roughness = 1
        
        # Motion Blur Config
        bpy.context.scene.eevee.use_motion_blur = False

        # Shadows Config
        bpy.context.scene.eevee.shadow_cube_size = '128'
        bpy.context.scene.eevee.shadow_cascade_size = '256'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True
        bpy.context.scene.eevee.use_soft_shadows = True
        
        # Volumetrics Config
        bpy.context.scene.eevee.volumetric_tile_size = '16'
        bpy.context.scene.eevee.volumetric_samples = 32
        bpy.context.scene.eevee.use_volumetric_lights = True
        bpy.context.scene.eevee.use_volumetric_shadows = False
        
        # Metadata Config
        bpy.context.scene.render.use_stamp_date = True
        bpy.context.scene.render.use_stamp_time = False
        bpy.context.scene.render.use_stamp_render_time = False
        bpy.context.scene.render.use_stamp_frame = True
        bpy.context.scene.render.use_stamp_frame_range = False
        bpy.context.scene.render.use_stamp_memory = False
        bpy.context.scene.render.use_stamp_hostname = False
        bpy.context.scene.render.use_stamp_camera = True
        bpy.context.scene.render.use_stamp_lens = True
        bpy.context.scene.render.use_stamp_scene = False
        bpy.context.scene.render.use_stamp_marker = False
        bpy.context.scene.render.use_stamp_filename = True
        bpy.context.scene.render.use_stamp_sequencer_strip = False
        
        # Stamp Config
        bpy.context.scene.render.use_stamp = True
        bpy.context.scene.render.stamp_font_size = 24

        # Render Config
        bpy.context.scene.eevee.taa_render_samples = 8
        bpy.context.scene.eevee.taa_samples = 8       
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        
        # Output Config
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'NONE'
        bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
        bpy.context.scene.render.ffmpeg.gopsize = 25
        bpy.context.scene.render.ffmpeg.video_bitrate = 12000
        bpy.context.scene.render.ffmpeg.minrate = 12000
        bpy.context.scene.render.ffmpeg.maxrate = 12000
        bpy.context.scene.render.ffmpeg.buffersize = 2000
        
        # Audio Config
        bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'
        bpy.context.scene.render.ffmpeg.audio_channels = 'STEREO'
        
        # CP Config
        bone_name = "c_pos"
        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                keys_list = list(c_pos_bone.keys())
                for lrprop in keys_list:
                    if lrprop not in ['_RNA_UI']:
                        if lrprop.startswith("001-CantidadPelo"):
                            if "_RNA_UI" not in c_pos_bone:
                                c_pos_bone["_RNA_UI"] = {}
                            if "001-CantidadPelo" not in c_pos_bone["_RNA_UI"]:
                                c_pos_bone["_RNA_UI"]["001-CantidadPelo"] = {}
                            c_pos_bone["_RNA_UI"]["001-CantidadPelo"]["max"] = 1.0
                            c_pos_bone["_RNA_UI"]["001-CantidadPelo"]["min"] = 0.0
                            c_pos_bone[lrprop] = 1.0
                            obj.update_tag(refresh={'OBJECT'})
        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                for lrpropcm in c_pos_bone.keys():
                    if lrpropcm not in ['_RNA_UI']:
                        if lrpropcm.startswith("002-CorneaMask"):
                            c_pos_bone[lrpropcm] = 1
                            obj.update_tag(refresh={'OBJECT'})
        bpy.context.view_layer.update()

        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                for vrpropvm in c_pos_bone.keys():
                    if vrpropvm not in ['_RNA_UI']:
                        if vrpropvm.startswith("VisorMask"):
                            c_pos_bone[vrpropvm] = 1
                            obj.update_tag(refresh={'OBJECT'})
        bpy.context.view_layer.update()

        for obj in bpy.data.objects:
            name = obj.name.lower().replace("ó", "o")
            if name == "vegetacion":
                obj.hide_viewport = False
            if obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION' and obj.instance_collection:
                instance_name = obj.instance_collection.name.lower().replace("ó", "o")
                if instance_name == "vegetacion":
                    obj.hide_viewport = False
        for collection in bpy.data.collections:
            name = collection.name.lower().replace("ó", "o")
            if name == "vegetacion":
                collection.hide_viewport = False
        bpy.context.view_layer.update()
        
        return {'FINISHED'}
    
class FRSettingsOp(bpy.types.Operator):
    bl_label = "Render Final"
    bl_description = "Configura la Escena para Renderizar bajo cierto preset"
    bl_idname = 'object.fr_operator'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"
    
    def execute(self, context):
        # Simplyfy config
        bpy.context.scene.render.use_simplify = False
        
        # Curves Config
        bpy.context.scene.render.hair_type = 'STRIP'
        bpy.context.scene.render.hair_subdiv = 3    
                
        # DOF Config
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
        bpy.context.scene.eevee.use_bokeh_jittered = True
        bpy.context.scene.eevee.bokeh_overblur = 20
        
        # SSR Config
        bpy.context.scene.eevee.use_ssr = True
        bpy.context.scene.eevee.use_ssr_refraction = True
        bpy.context.scene.eevee.use_ssr_halfres = True
        bpy.context.scene.eevee.ssr_quality = 0.25
        bpy.context.scene.eevee.ssr_max_roughness = 0.5
                
        # Motion Blur Config
        bpy.context.scene.eevee.use_motion_blur = False
        
        # Shadows Config
        bpy.context.scene.eevee.shadow_cube_size = '1024'
        bpy.context.scene.eevee.shadow_cascade_size = '2048'
        bpy.context.scene.eevee.use_shadow_high_bitdepth = True
        bpy.context.scene.eevee.use_soft_shadows = True
        
        # Volumetrics Config
        bpy.context.scene.eevee.volumetric_tile_size = '8'
        bpy.context.scene.eevee.volumetric_samples = 64
        bpy.context.scene.eevee.use_volumetric_lights = True
        bpy.context.scene.eevee.use_volumetric_shadows = True
        
        # Metadata Config
        bpy.context.scene.render.use_stamp_date = True
        bpy.context.scene.render.use_stamp_time = False
        bpy.context.scene.render.use_stamp_render_time = False
        bpy.context.scene.render.use_stamp_frame = True
        bpy.context.scene.render.use_stamp_frame_range = False
        bpy.context.scene.render.use_stamp_memory = False
        bpy.context.scene.render.use_stamp_hostname = False
        bpy.context.scene.render.use_stamp_camera = True
        bpy.context.scene.render.use_stamp_lens = True
        bpy.context.scene.render.use_stamp_scene = False
        bpy.context.scene.render.use_stamp_marker = False
        bpy.context.scene.render.use_stamp_filename = True
        bpy.context.scene.render.use_stamp_sequencer_strip = False
        
        # Stamp Config
        bpy.context.scene.render.use_stamp = False
        
        # Render Config
        bpy.context.scene.eevee.taa_render_samples = 64
        bpy.context.scene.eevee.taa_samples = 8
        bpy.context.scene.render.resolution_x = 3840
        bpy.context.scene.render.resolution_y = 2160
        
        # Output Config
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'QUICKTIME'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'NONE'
        bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'BEST'
        bpy.context.scene.render.ffmpeg.video_bitrate = 200000
        bpy.context.scene.render.ffmpeg.minrate = 200000
        bpy.context.scene.render.ffmpeg.maxrate = 200000
        bpy.context.scene.render.ffmpeg.buffersize = 2000
        
        # Audio Config
        bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'
        bpy.context.scene.render.ffmpeg.audio_channels = 'STEREO'
        
    
        # CP Config
        bone_name = "c_pos"
        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                keys_list = list(c_pos_bone.keys())
                for frprop in keys_list:
                    if frprop not in ['_RNA_UI']:
                        if frprop.startswith("001-CantidadPelo"):
                            if "_RNA_UI" not in c_pos_bone:
                                c_pos_bone["_RNA_UI"] = {}
                            if "001-CantidadPelo" not in c_pos_bone["_RNA_UI"]:
                                c_pos_bone["_RNA_UI"]["001-CantidadPelo"] = {}
                            c_pos_bone["_RNA_UI"]["001-CantidadPelo"]["min"] = 0.0
                            c_pos_bone["_RNA_UI"]["001-CantidadPelo"]["max"] = 1.0
                            c_pos_bone[frprop] = 1.0
                            obj.update_tag(refresh={'OBJECT'})
        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                for frpropcm in c_pos_bone.keys():
                    if frpropcm not in ['_RNA_UI']:
                        if frpropcm.startswith("002-CorneaMask"):
                            c_pos_bone[frpropcm] = 1 
                            obj.update_tag(refresh={'OBJECT'})
        bpy.context.view_layer.update()

        for obj in bpy.context.scene.objects:
           if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                for vrpropvm in c_pos_bone.keys():
                    if vrpropvm not in ['_RNA_UI']:
                        if vrpropvm.startswith("VisorMask"):
                            c_pos_bone[vrpropvm] = 1
                            obj.update_tag(refresh={'OBJECT'})
        bpy.context.view_layer.update()

        for obj in bpy.data.objects:
            name = obj.name.lower().replace("ó", "o")
            if name == "vegetacion":
                obj.hide_viewport = False
            if obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION' and obj.instance_collection:
                instance_name = obj.instance_collection.name.lower().replace("ó", "o")
                if instance_name == "vegetacion":
                    obj.hide_viewport = False
        for collection in bpy.data.collections:
            name = collection.name.lower().replace("ó", "o")
            if name == "vegetacion":
                collection.hide_viewport = False
        bpy.context.view_layer.update()
        
        return {'FINISHED'}

class FloorTarget(bpy.types.Panel):
    bl_label = "Floor Obj"
    bl_idname = "OBJECT_PT_select_piso"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text = f"Aplicar Piso")
        box.operator('object.floor_operator')

class ConfigureGlobalyNeededProperties(bpy.types.Panel):
    bl_label = "Custom Properties Globales"
    bl_idname = "OBJECT_PT_configure_global_custom_properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        bone_name = "c_pos"

        box = layout.box()
        box.label(text=f"Cantidad de Pelo:")
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]


                for prop in c_pos_bone.keys():
                    if prop not in ['_RNA_UI']:
                        if prop.startswith("001-CantidadPelo"):
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=obj.name, slider=True)

        box = layout.box()
        box.label(text=f"Mascaras de Cornea")
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                
                
                for prop in c_pos_bone.keys():
                    if prop not in ['_RNA_UI']:
                        if prop.startswith("002-CorneaMask"):
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=obj.name)

        box = layout.box()
        box.label(text=f"Control Squash & Stretch")
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                        
                        
                for prop in c_pos_bone.keys():
                    if prop not in ['_RNA_UI']:
                        if prop.startswith("000-S&S"):
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=obj.name)

        box = layout.box()
        box.label(text=f"Control Pisadas")
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                        
                        
                for prop in c_pos_bone.keys():
                    if prop not in ['_RNA_UI']:
                        if prop.startswith("000-Pisada"):
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=obj.name)

class ConfigureCustomPropertiesPanel(bpy.types.Panel):
    bl_label = "Lista de Custom Properties"
    bl_idname = "OBJECT_PT_configure_general_custom_properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Properties"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        bone_name = "c_pos"

        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and bone_name in obj.pose.bones:
                c_pos_bone = obj.pose.bones[bone_name]
                box = layout.box()
                box.label(text=f"{obj.name} - {bone_name} Custom Properties:")

                for prop in c_pos_bone.keys():
                    if prop not in ['_RNA_UI']:
                        if prop.startswith("001-CantidadPelo"):
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=prop, slider=True)
                        elif prop.startswith("002-CorneaMask"):
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=prop)
                        else:
                            box.prop(c_pos_bone, '["{}"]'.format(prop), text=prop)

class UpdateConfig(bpy.types.AddonPreferences):
    bl_idname = __package__
    # addon updater preferences from `__init__`, be sure to copy all of them
    auto_check_update = bpy.props.BoolProperty(
        name = "Auto-check for Update",
        description = "If enabled, auto-check for updates using an interval",
        default = False,
    )

    updater_interval_months = bpy.props.IntProperty(
        name='Months',
        description = "Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_interval_days = bpy.props.IntProperty(
        name='Days',
        description = "Number of days between checking for updates",
        default=7,
        min=0,
    )
    updater_interval_hours = bpy.props.IntProperty(
        name='Hours',
        description = "Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_interval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description = "Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )
        
    def draw(self,context):
        layout = self.layout
        addon_updater_ops.update_settings_ui(self,context)
       
clases = (
    FloorTarget,
    VRSettingsOp,
    LRSettingsOp,
    FRSettingsOp,
    RenderSettingsB,
    ConfigureCustomPropertiesPanel,
    ConfigureGlobalyNeededProperties,
    UpdateConfig
)

def register():
    addon_updater_ops.register(bl_info)
    for clase in clases:
        bpy.utils.register_class(clase)

def unregister():
    for clase in clases:
        bpy.utils.unregister_class(clase)
  
if __name__ == "main":
    register()