## So what to do
# get all images in syn_images_cropped_bkg_overlaid
# for each, get visible points
# change renderparams to get deltas
# get the 4 way map
# save the 4way map
import os
import sys
sys.path.insert(0,'../data_creator')
import utils
import io_utils
import numpy as np
import variables as v
loc_map = {'chair':'03001627/13fdf00cde077f562f6f52615fb75fca',
          'sofa':'04256520/2bb1b5865455b2b814513156cf2b8d0d',
          'bed':'02818832/7c8eb4ab1f2c8bfa2fb46fb8b9b1ac9f',
          'diningtable':'04379243/e41da371550711697062f2d72cde5c95'}
map_loc = {'03001627':('Chair','13fdf00cde077f562f6f52615fb75fca',),
          '04256520':('Sofa','2bb1b5865455b2b814513156cf2b8d0d'),
          '02818832':('Bed','7c8eb4ab1f2c8bfa2fb46fb8b9b1ac9f'),
           '04379243':('Diningtable','e41da371550711697062f2d72cde5c95')
          }
k = 2

def get_image_paths(path_to_img,no_path=False):
    #level_1 =[os.path.join(path_to_img,x) for x in os.listdir(path_to_img)]
    level_1 =[os.path.join(path_to_img,x) for x in ['04379243',]]
    level_2 = [os.path.join(x,y) for x in level_1 for y in os.listdir(x)]
    level_3 = [os.path.join(x,y) for x in level_2 for y in os.listdir(x)]
    if no_path:
        print(len(path_to_img))
        level_3 = [x[len(path_to_img)+1:] for x in level_3]
    return level_3


path_image_1_folder = 'data/final_dataset_texture/syn_images_cropped_bkg_overlaid'
save_loc = '/home/aditya/projects/siggraph/flows/syn_flow'
corr_loc = '../data/sample_points'
def main():
    #for class_name in loc_map.values():
    #    if not os.path.exists(os.path.join(save_loc,class_name.split('/')[0])):
    #        os.mkdir(os.path.join(save_loc,class_name.split('/')[0]))
    #    if not os.path.exists(os.path.join(save_loc,class_name)):
    #        os.mkdir(os.path.join(save_loc,class_name))
    #print('made_dir')
    obj_1_image_names = get_image_paths(os.path.join('..',path_image_1_folder),True)
    print(len(obj_1_image_names))

    ## need to load a correlation file 
    
    for cur_obj_1 in obj_1_image_names:
    #cur_obj_1 = obj_1_image_names[20]
        obj = cur_obj_1.split('/')[0]
        corr_file = os.path.join(corr_loc,'_'.join([obj,map_loc[obj][1]+'.npy'] ) )
        x1 = io_utils.get_params_from_file(cur_obj_1)
        depth_name_1 = os.path.join('..','/'.join(path_image_1_folder.split('/')[:-1]),'syn_depth')
        # now get the points render
        #model_1_pts,_ = io_utils.get_point_arrays(corr_file,True)
        model_1_pts = np.load(corr_file)
        print(model_1_pts.shape,'the shape of you')
        truth_1,crop_pt_array_1 =  io_utils.get_render_array(x1,model_1_pts,depth_name_1)
        #crop_pt_array_1 = crop_pt_array_1[:,truth_1]
        # now for one direction
        print('model',model_1_pts.shape)
        #model_1_pts = model_1_pts[truth_1,:]
        print('model',model_1_pts.shape)
        crop_pt_array_1 =  io_utils.get_render_array_no_prune(x1,model_1_pts)
        x1['azimuth'] +=10
        x1['elevation'] +=10
        crop_pt_array_azi =  io_utils.get_render_array_no_prune(x1,model_1_pts)
        # now for each of these we can generate 4 maps
        #crop_pt_array_azi[0,:] -= (np.min(crop_pt_array_azi[0,:])-np.min(crop_pt_array_1[0,:]))
        #crop_pt_array_azi[1,:] -= (np.min(crop_pt_array_azi[1,:])-np.min(crop_pt_array_1[1,:]))
        #crop_pt_array_ele[0,:] -= (np.min(crop_pt_array_ele[0,:])-np.min(crop_pt_array_1[0,:]))
        #crop_pt_array_ele[1,:] -= (np.min(crop_pt_array_ele[1,:])-np.min(crop_pt_array_1[1,:]))

        del_azi = crop_pt_array_azi -crop_pt_array_1
        print(np.max(del_azi))

        flow = np.zeros((224,224,2))
        x1 = io_utils.get_params_from_file(cur_obj_1)
        truth_1,crop_pt_array_1 =  io_utils.get_render_array(x1,model_1_pts,depth_name_1)
        for i in range(crop_pt_array_1.shape[1]):
            if truth_1[i]:
                pt = crop_pt_array_1[:,i][:2].astype(int)
                flow[pt[1]-k:pt[1]+k,pt[0]-k:pt[0]+k,0] = del_azi[:,i][0]
                flow[pt[1]-k:pt[1]+k,pt[0]-k:pt[0]+k,1] = del_azi[:,i][1]
        print(flow.shape,'Done!')
        np.save(os.path.join(save_loc,cur_obj_1),flow)
if __name__ == '__main__':
    main()