# Blender Intrinsic Camera parameters
# Voxel to world coordinate matrix
# function for extrinsic camera matrix from 3 angles and rho
import binvox_rw
import itertools
from scipy.spatial import ConvexHull
import numpy as np
class vox2render:
    '''
    Class containing model information for mapping each voxel to each render
    * Voxel location array[(x,y,z)], size and translation from binox-rw-py
    * Each voxel to render mapper function
    * Each voxel Visibility Function
      * Voxel 2D projection (convex hull of 8 vertices)
      * Intersection based visibility assesment
    * Voxel to global VOX mapper
    '''
    def __init__(self,file_name):
        file = open(file_name, 'rb')
        self.vox_array = binvox_rw.read_as_coord_array(file)
        self.tot_vox = self.vox_array.data.shape[1]
        self.adjusted_vox_array = self.make_adjusted_vox_array()
        self.vox_global_map = None
        
        
    def make_adjusted_vox_array(self,vox_array = None):
        if vox_array==None:
            vox_array = self.vox_array.data
        vox_ar = np.copy(vox_array/128.0*self.vox_array.scale + np.array(self.vox_array.translate)[:,None])
        return vox_ar
    
    def give_render_location(self,camera_matrix,obj_to_world_matrix,vox_array= None):
        proj_list = []
        if vox_array == None:
            vox_array = self.adjusted_vox_array
        for i in range(vox_array.shape[1]):
            vox = np.ones((4,1),dtype='float')
            vox[0:3,0:1]= vox_array[:,i:i+1]
            vox = np.matmul(obj_to_world_matrix,vox)
        
            vox_proj = np.matmul(camera_matrix,vox)[:,0]
            depth = np.copy(vox_proj[2])
            # print(depth)
            vox_proj = vox_proj/depth
            vox_proj[2] = np.copy(depth)
            vox_proj[0:2] = np.round(vox_proj[0:2])
            proj_list.append(vox_proj)
        
        return np.array(proj_list)
    
    def give_visibility_index(self,render_locations,im_crop_params=[0,540,0,960]):
        ## will use to functions
        top = im_crop_params[0]
        bottom = im_crop_params[1]
        left = im_crop_params[2]
        right = im_crop_params[3]
        image_plane = np.zeros((bottom-top,right-left))
        # Start checking from closest point 
        dict_order = {tuple(render_locations[i,:]):i for i in range(self.tot_vox)}
        dict_visi = {tuple(render_locations[i,:]):False for i in range(self.tot_vox)}
        render_locations = render_locations[render_locations[:,2].argsort()]
        for i in range(self.tot_vox):
            # check if inside crop
            cur_render = render_location[i,:]
            cur_vox = self.vox_array.data[:,i]
            if (cur_render[0]> bottom and cur_render[0]< top and cur_render[1]> left and cur_render[1]< right ):
                # get the 8 vertices
                vertice_list = get_adjusted_vertex(cur_vox)
                rendered_vertex = give_render_location(camera_matrix,obj_to_world_matrix,vertice_list)
                # get convx hull
                
                # get np array with covering polygon
                # Try if this alone is sufficient
            else:
                print('mama')
                
    def get_adjusted_vertex(self,cur_vox):
        vertice_list = []
        for x,y,z in itertools.product(range(2),range(2),range(2)):
            vertice_list.append(cur_vox + np.array([(-0.5+x),(-0.5+y),(-0.5+z)]))
        vertice_list.append(cur_vox)
        vertice_list = np.array(vertice_list)
        # print(vertice_list)
        adjusted_vertice_list = self.make_adjusted_vox_array(np.transpose(vertice_list))
        return adjusted_vertice_list
        
