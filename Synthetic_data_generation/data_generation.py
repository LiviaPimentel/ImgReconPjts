import bpy
import numpy as np
import time
import math as m
import os
import random

class Render:
    def __init__(self):
        # Scene information
        self.scene = bpy.data.scenes['Scene']
        self.camera = bpy.data.objects['Camera']
        self.axis = bpy.data.objects['Empty']
        self.light_1 = bpy.data.objects['Light']
        #self.light_2 = bpy.data.objects['Light.001']
        #self.obj_names = ['Arrow', 'Cross', 'Square', 'Triangle']
        self.obj_names = ['0', '1', '2', '3']
        self.objects = self.create_objects()
        self.textin = ''

        # Render information
        self.camera_z_limits = [20, 40]
        self.axis_x_rot_limit = [30, -20]
        self.axis_y_rot_limit = [30, -20]
        self.axis_z_rot_limit = [0, 360]

        # Output information
        self.images_filepath = 'C:/Users/livia/Documents/Blender_models/imgs/'
        self.label_imgs_filepath = 'C:/Users/livia/Documents/Blender_models/labels/'
                                   
    def create_objects(self):
        objs = []
        for obj in self.obj_names:
            objs.append(bpy.data.objects[obj])
        
        return objs

    def find_bounding_box(self, obj):
        """
        Returns camera space bounding box of the mesh object.

        Gets the camera frame bounding box, which by default is returned without any transformations applied.
        Create a new mesh object based on self.carre_bleu and undo any transformations so that it is in the same space as the
        camera frame. Find the min/max vertex coordinates of the mesh visible in the frame, or None if the mesh is not in view.

        :param scene:
        :param camera_object:
        :param mesh_object:
        :return:
        """

        """ Get the inverse transformation matrix. """
        matrix = self.camera.matrix_world.normalized().inverted()
        """ Create a new mesh data block, using the inverse transform matrix to undo any transformations. """
        mesh = obj.to_mesh(preserve_all_data_layers=True)
        mesh.transform(obj.matrix_world)
        mesh.transform(matrix)

        """ Get the world coordinates for the camera frame bounding box, before any transformations. """
        frame = [-v for v in self.camera.data.view_frame(scene=self.scene)[:3]]

        lx = []
        ly = []

        for v in mesh.vertices:
            co_local = v.co
            z = -co_local.z

            if z <= 0.0:
                """ Vertex is behind the camera; ignore it. """
                continue
            else:
                """ Perspective division """
                frame = [(v / (v.z / z)) for v in frame]

            min_x, max_x = frame[1].x, frame[2].x
            min_y, max_y = frame[0].y, frame[1].y

            x = (co_local.x - min_x) / (max_x - min_x)
            y = (co_local.y - min_y) / (max_y - min_y)

            lx.append(x)
            ly.append(y)

        # bpy.data.meshes.remove(mesh)

        """ Image is not in view if all the mesh verts were ignored """
        if not lx or not ly:
            return None

        min_x = np.clip(min(lx), 0.0, 1.0)
        min_y = np.clip(min(ly), 0.0, 1.0)
        max_x = np.clip(max(lx), 0.0, 1.0)
        max_y = np.clip(max(ly), 0.0, 1.0)

        """ Image is not in view if both bounding points exist on the same side """
        if min_x == max_x or min_y == max_y:
            return None

        """ Figure out the rendered image size """
        render = self.scene.render
        fac = render.resolution_percentage * 0.01
        dim_x = render.resolution_x * fac
        dim_y = render.resolution_y * fac
        
        ## Verify there's no coordinates equal to zero
        coord_list = [min_x, min_y, max_x, max_y]
        if min(coord_list) == 0.0:
            indexmin = coord_list.index(min(coord_list))
            coord_list[indexmin] = coord_list[indexmin] + 0.0000001

        return (min_x, min_y), (max_x, max_y)

    def format_coordinates(self, coordinates, classe, resx, resy):
        if coordinates:
            x1 = (coordinates[0][0])
            x2 = (coordinates[1][0])
            y1 = (1-coordinates[1][1])
            y2 = (1-coordinates[0][1])
            # self.obj_names = ['Arrow', 'Cross', 'Square', 'Triangle']

            #print('minX:', x1, 'minY:', y1, '\nmaxX:', x2, 'maxY:', y2)
            final_coordinates = {'class': str(classe), 'Xmin': x1, 'Ymin':y1,'Xmax': x2, 'Ymax': y2}
            txt_coordinates = self.obj_names[classe].replace(' ','_') +' '+str(x1*resx)+' '+str(y1*resy)+' '+str(x2*resx)+' '+str(y2*resy)+'\n'
            
            return final_coordinates, txt_coordinates
        
        else:
            pass

    def get_all_coordinates(self, resx, resy):
        main_label_dict = {}
        main_text_coordinates = ''
        for i, obj in enumerate(self.objects):
            b_box = self.find_bounding_box(obj)
            if b_box:
                cur_coordinates = self.format_coordinates(b_box, i, resx, resy)[0]
                text_coordinates = self.format_coordinates(b_box, i, resx, resy)[1]
                main_label_dict[self.obj_names[i]] = cur_coordinates
                main_text_coordinates = main_text_coordinates+text_coordinates
    
        return main_label_dict, main_text_coordinates

    def set_camera(self):
        self.axis.rotation_euler = (0, 0, 0)
        self.axis.location = (0, 0, 0)
        self.camera.location = (0, 0, 3)
    
    def calculate_n_renders(self, rotation_step):
        zmin = int(self.camera_z_limits[0] * 10)
        zmax = int(self.camera_z_limits[1] * 10)

        render_counter = 1
        rotation_step = rotation_step

        for d in range(zmin, zmax+1, 2):
            camera_location = (0,0,d/10)
            #print('Camera location at:', camera_location)
            render_counter +=1
            min_thetax = (-1)*self.axis_x_rot_limit[0] + 90
            max_thetax = (-1)*self.axis_x_rot_limit[1] + 90

            for thetax in range(min_thetax, max_thetax+1,rotation_step):
                thetax_r = 90 - thetax
                render_counter +=1
                min_thetay = (-1) * self.axis_y_rot_limit[0] + 90
                max_thetay = (-1) * self.axis_y_rot_limit[1] + 90

                for thetaz in range(self.axis_z_rot_limit[0], self.axis_z_rot_limit[1]+1,rotation_step):
                    render_counter += 1
                    axis_rotation = (thetax_r, 0, thetaz)
                    #print('Axis rotation at:', axis_rotation)

        return render_counter
    
    def main_rendering_loop(self, rot_step):
        n_renders = self.calculate_n_renders(rot_step)
        print('Number of renders to create:', n_renders)
        
        accept_render = input('\nContinue?[Y/N]:  ')
        
        if accept_render == 'Y':
            report_file_path = self.label_imgs_filepath + '/progress_report.txt'
            zmin = int(self.camera_z_limits[0] * 10)
            zmax = int(self.camera_z_limits[1] * 10)

            render_counter = 1
            rotation_step = rot_step
        
            report = open(report_file_path, 'w')
            
            for d in range(zmin, zmax+1, 2):
                self.camera.location = (0,0,d/10)
                render_counter +=1
                min_thetax = (-1)*self.axis_x_rot_limit[0] + 90
                max_thetax = (-1)*self.axis_x_rot_limit[1] + 90

                for thetax in range(min_thetax, max_thetax+1,rotation_step):
                    thetax_r = 90 - thetax
                    render_counter +=1
                    min_thetay = (-1) * self.axis_y_rot_limit[0] + 90
                    max_thetay = (-1) * self.axis_y_rot_limit[1] + 90

                    for thetaz in range(self.axis_z_rot_limit[0], self.axis_z_rot_limit[1]+1,rotation_step):
                        render_counter += 1
                        axis_rotation = (m.radians(thetax_r), 0, m.radians(thetaz))
                        #print('Axis rotation at:', axis_rotation)
                        self.axis.rotation_euler = axis_rotation
                        self.render_blender(render_counter)
                        
                        ## Configure lighting
                        self.light_1 = random.randint(1,100)
                        print('light1=', self.light_1)
                        self.light_2 = random.randint(1,100)
                        print('light2=', self.light_2)
                        
                        ## Output Labels
                        text_file_name = self.images_filepath+'/'+str(render_counter)+'.txt'
                        text_file = open(text_file_name, 'w+')
                        text_coordinates = self.get_all_coordinates(self.xpix*self.percentage*0.01, self.ypix*self.percentage*0.01)[1]
                        splitted_coordinates = text_coordinates.split('\n')[:-1]
                        text_file.write('\n'.join(splitted_coordinates))
                        text_file.close()
                        
                        ## Show progress on batch of renders
                        print('Progress =', str(render_counter) + '/' + str(n_renders))
                        
                        report.write('Progress: '+str(render_counter)+' Rotation: '+str(axis_rotation)+' z_d: '+str(d/10)+'\n')
                        
            report.close()
        
        else:
            print('Aborted rendering operation')
            pass         
        
        
    def render_blender(self, count_f_name):
        # Define random parameters
        random.seed(random.randint(1,1000))
        self.xpix = random.randint(500, 1500)
        self.ypix = random.randint(500, 1500)
        self.percentage = random.randint(25, 100)
        samples = random.randint(25, 100) 
        
        # Render images
        image_name = str(count_f_name) + '.png'
        self.export_render(self.xpix, self.ypix, self.percentage, samples, self.images_filepath, image_name)
        self.export_render(self.xpix, self.ypix, 25, 25, self.label_imgs_filepath, image_name)
        label_img = self.label_imgs_filepath+'/'+image_name
    
    def drawBoundingBox(self, result):
        x1=result['topleft']['x']
        y1=result['topleft']['y']
        x2=result['bottomright']['x']
        y2=result['bottomright']['y']

        print('Current image size is:', self.image_shape)
        label = result['label']

        cv2.rectangle(self.image, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0),int(6))
        labelSize = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, 0.5, 2)
        # print('labelSize>>',labelSize)
        _x1 = x1
        _y1 = y1  # +int(labelSize[0][1]/2)
        _x2 = _x1 + labelSize[0][0]
        _y2 = y1 - int(labelSize[0][1])
        cv2.rectangle(self.image, (int(_x1), int(_y1)), (int(_x2), int(_y2)), (0, 255, 0), cv2.FILLED)
        cv2.putText(self.image, label, (int(x1), int(y1)), cv2.FONT_HERSHEY_COMPLEX, 0.35, (0, 0, 0), 1)

        return self.image

    def export_render(self, res_x, res_y, res_per, samples, file_path, file_name):
        bpy.context.scene.cycles.samples = samples
        self.scene.render.resolution_x = res_x
        self.scene.render.resolution_y = res_y
        self.scene.render.resolution_percentage = res_per
        self.scene.render.filepath =  file_path + '/' + file_name

        bpy.ops.render.render(write_still=True)

r = Render()
r.set_camera()
r.main_rendering_loop(30)
