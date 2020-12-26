import os
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image
from PIL import ImageFilter

def gray_to_rgb(image):
    """
    convert a gray-scale image to RGB image

    image: an input 2D numpy array with shape [H, W]
    image_cat: a output numpy array with shape [H, W, 3]
    """
    image_cat = np.asarray([image, image, image])
    image_cat = np.transpose(image_cat, [1, 2, 0])
    return image_cat


def get_slice_from_volume(image, view, slice_id):
    """
    extract a slice form a volume image

    image: a 3D numpy array with shape of [D, H, W]
    view : 0 -- axial, 1 -- sagittal, 2 -- coronal
    slice_id: slice index in the given view
    """
    if(view == 1):
        image = np.transpose(image, [2, 0, 1])
    elif(view == 2):
        image = np.transpose(image, [1, 0, 2])
    return image[slice_id]


def add_contour(In, Seg, Color=(0, 255, 0)):
    """
    add segmentation contour to an input image

    In: Input PIL.Image object, should be an RGB image
    Seg: segmentation mask represented by a PIL.Image object
    Color: a vector specifying the color of contour
    Out: output PIL.Image object with segmentation contour overlayed
    """
    Out = In.copy()
    [H, W] = In.size
    for i in range(H):
        for j in range(W):
            if(i==0 or i==H-1 or j==0 or j == W-1):
                if(Seg.getpixel((i,j))!=0):
                    Out.putpixel((i,j), Color)
            elif(Seg.getpixel((i,j))!=0 and  \
                 not(Seg.getpixel((i-1,j))!=0 and \
                     Seg.getpixel((i+1,j))!=0 and \
                     Seg.getpixel((i,j-1))!=0 and \
                     Seg.getpixel((i,j+1))!=0)):
                     Out.putpixel((i,j), Color)
                     Out.putpixel((i+1,j), Color)
                     Out.putpixel((i,j+1), Color)
                     Out.putpixel((i-1,j), Color)
                     Out.putpixel((i,j-1), Color)
    return Out

def add_segmentation_color(In, Seg, Color=(255, 0, 0), alpha=0.3):
    """
    add segmentation mask to an input image

    In: Input PIL.Image object, should be an RGB image
    Seg: segmentation mask represented by a PIL.Image object
    Color: a vector specifying the color of contour
    alpha: alpha value of the mask
    Out: output PIL.Image object with segmentation contour overlayed
    """
    Out = In.copy()
    [H, W] = In.size
    for i in range(H):
        for j in range(W):
            fg = Seg.getpixel((i,j))
            if(fg>0):
                color0 = In.getpixel((i,j))
                color1 = (int(color0[0] * (1.0 - alpha) + Color[0] * alpha),
                          int(color0[1] * (1.0 - alpha) + Color[1] * alpha),
                          int(color0[2] * (1.0 - alpha) + Color[2] * alpha))
                Out.putpixel((i,j), color1)                    
    return Out

def get_central_slice_index_of_nonzero_region(image, view):
    """
    get the central slice index of nonzero region of a volume 3D

    image: a 3D numpy array
    view : 0 -- axial, 1 -- sagittal, 2 -- coronal
    """
    [d_index, h_index, w_index] = np.where(image)
    if(view == 0):
        index_list = d_index
    elif(view == 1):
        index_list = w_index
    else:
        index_list = h_index
    idx_min = min(index_list)
    idx_max = max(index_list)
    i_cen = int((idx_min + idx_max)/2)
    return i_cen

def map_scalar_to_color(x):
    x_list = [0.0, 0.25, 0.5, 0.75, 1.0]
    c_list = [[0, 0, 255],
              [0, 255, 255],
              [0, 255, 0],
              [255, 255, 0],
              [255, 0, 0]]
    for i in range(len(x_list)):
        if(x <= x_list[i + 1]):
            x0 = x_list[i]
            x1 = x_list[i + 1]
            c0 = c_list[i]
            c1 = c_list[i + 1]
            alpha = (x - x0)/(x1 - x0)
            c = [c0[j]*(1 - alpha) + c1[j] * alpha for j in range(3)]
            c = [int(item) for item in c]
            return tuple(c)

def show_one_slice(img_folder, lab_folder, method_list, seg_folder_list, img_id, view_id,
         slice_id, save_dir = None, contour = False):
    img_name = "{0:}/{1:}.nii.gz".format(img_folder, img_id)
    lab_name = "{0:}/{1:}.nii.gz".format(lab_folder, img_id)
    img_obj = sitk.ReadImage(img_name)
    spacing = img_obj.GetSpacing()
    scale   = spacing[2]/spacing[0]
    img = sitk.GetArrayFromImage(img_obj)

    # Rescale the image intensity to [0,255].
    # You may need to edit this according to your data
    img = (img + 1400) / 1500 * 255
    img[img < 0]   = 0
    img[img > 255] = 255
    img = np.asarray(img, np.uint8)

    # Extract the specified slice from the image and ground truth mask
    lab_obj = sitk.ReadImage(lab_name)
    lab     = sitk.GetArrayFromImage(lab_obj)
    img_slc = get_slice_from_volume(img, view_id, slice_id)
    lab_slc = get_slice_from_volume(lab, view_id, slice_id)
 
    im_show_raw = gray_to_rgb(img_slc)
    im_show_raw = Image.fromarray(im_show_raw)
    lab_slc = Image.fromarray(lab_slc)
    
    # As the 3D resolution may be anisotropic, resampleing to isotropic
    # resolution is needed for better visualization
    if(view_id == 1 or view_id == 2):
        new_size = [im_show_raw.size[0], int(im_show_raw.size[1] * scale)]
        im_show_raw = im_show_raw.resize(new_size)
        lab_slc = lab_slc.resize(new_size)        

    seg_list = []
    for seg_folder in seg_folder_list:
        seg_name = "{0:}/{1:}.nii.gz".format(seg_folder, img_id)
        seg_obj = sitk.ReadImage(seg_name)
        seg     = sitk.GetArrayFromImage(seg_obj)
        seg_slc = get_slice_from_volume(seg, view_id, slice_id)
        seg_slc = Image.fromarray(seg_slc)
        if(view_id == 1 or view_id == 2):
            seg_slc = seg_slc.resize(new_size)   
        seg_list.append(seg_slc)
    
    plt.figure(figsize=(15, 8))
    im_show = im_show_raw
    if(contour):
        im_show = add_contour(im_show, lab_slc, (255, 128, 0))
        im_gt   = im_show 
    else:
        im_gt   = add_segmentation_color(im_show, lab_slc)
    N  = len(seg_list)
    column = int((N + 3) / 2)
    plt.subplot(2, column, 1); plt.axis("off")
    plt.imshow(im_show_raw); plt.title("image")
    plt.subplot(2, column, 2); plt.axis("off")
    plt.imshow(im_gt); plt.title("ground_truth")

    if(save_dir):
        save_name = "{0:}/{1:}_{2:}_img.png".format(save_dir, img_id, slice_id)
        im_show_raw.save(save_name)
        save_name = "{0:}/{1:}_{2:}_gt.png".format(save_dir, img_id, slice_id)
        im_gt.save(save_name)
    for n in range(N):
        plt.subplot(2, column, n + 3); plt.axis("off")
        if(contour):
            im_show_n = add_contour(im_show, seg_list[n])
        else:
            im_show_n = add_segmentation_color(im_show, seg_list[n])
        if(save_dir):
            save_name = "{0:}/{1:}_{2:}_{3:}_.png".format(save_dir,
                img_id, slice_id, method_list[n])
            im_show_n.save(save_name)
        plt.imshow(im_show_n); plt.title(method_list[n])

    plt.show()


def show_results_for_comparison():
    """
    show 3d segmentation results in axial, sagittal or coronal views
    """
    img_folder = "./image"
    lab_folder = "./label"
    seg_root = "./net_compare"
    methods  = ["unet", "unet_att" "unet3d", "vnet"]
    seg_folder_list  = ["unet2d/result", "unet_att/result", "unet3d/result", "vnet/result"]
    seg_folder_list = [seg_root + '/' + item for item in seg_folder_list]    

    save_dir= False #  "./image1" #   
    img_id  = "image1"
    view_id  = 0  # 0-axial, 1-sagittal, 2-coronal
    slice_id = 50

    show_one_slice(img_folder, lab_folder, methods, seg_folder_list,
          img_id, view_id, slice_id, save_dir, contour=False)


if __name__ == "__main__":
    show_results_for_comparison()
