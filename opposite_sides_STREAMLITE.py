# Importing essential libraries

from io import BytesIO
import random
import numpy as np     # Used for using multi-dimensional arrays , matrices and other mathematical functions
import os              # Operating System library to include system dependent functionality like clearing terminal , manipulating paths and interacting with operating system
import copy            # To copy array
from PIL import Image, ImageOps
import numpy as np
import streamlit as st
import zipfile

os.system("cls")     

RES_H = 0
RES_W = 0

img1_cubic= []
img2_cubic= []
change_in_img1 = False
count = 0

color_code = {"red":[255, 0, 0],"green":[0,255,0],"white":[255,255,255],"orange":[255, 153, 0],"blue":[0, 0, 255],"yellow":[255,255, 0]}
opp_color = {"white":"yellow","yellow":"white","green":"blue","blue":"green","orange":"red","red":"orange"}
corner_count = {"red":0, "blue":0, "orange":0, "yellow":0, "green":0, "white":0}
edge_count = {"red":0, "blue":0, "orange":0, "yellow":0, "green":0, "white":0}


def get_color(code):
    for key, val in color_code.items():
        if val == code:
            return key
    return None 


def clear_color_count():
    for key, val in edge_count.items():
        corner_count[key] = 0
        edge_count[key] = 0


def get_corner_code(i):
    corner_code = []
    corner_color = []
    corner_count[get_color(img1_cubic[i][0][0])] += 1
    corner_count[get_color(img1_cubic[i][0][2])] += 1
    corner_count[get_color(img1_cubic[i][2][0])] += 1
    corner_count[get_color(img1_cubic[i][2][2])] += 1

    corner_count[get_color(img2_cubic[i][0][0])] += 1
    corner_count[get_color(img2_cubic[i][0][2])] += 1
    corner_count[get_color(img2_cubic[i][2][0])] += 1
    corner_count[get_color(img2_cubic[i][2][2])] += 1

    for key, val in corner_count.items():
        if val != 0:
            corner_code.append(val)
            corner_color.append(key)
    
    clear_color_count()

    sorted_lists = sorted(zip(corner_code, corner_color), reverse=True)
    list1_sorted, list2_sorted = zip(*sorted_lists)

    corner_code = list(list1_sorted)
    corner_color = list(list2_sorted)

    return (corner_code, corner_color)


def find_and_replace(find, replace, i):
    global img1_cubic, img2_cubic
    if img1_cubic[i][0][0] == color_code[find]: img1_cubic[i][0][0] = color_code[replace]
    elif img1_cubic[i][0][2] == color_code[find]: img1_cubic[i][0][2] = color_code[replace]
    elif img1_cubic[i][2][0] == color_code[find]: img1_cubic[i][2][0] = color_code[replace]
    elif img1_cubic[i][2][2] == color_code[find]: img1_cubic[i][2][2] = color_code[replace]
    elif img2_cubic[i][0][0] == color_code[find]: img2_cubic[i][0][0] = color_code[replace]
    elif img2_cubic[i][0][2] == color_code[find]: img2_cubic[i][0][2] = color_code[replace]
    elif img2_cubic[i][2][0] == color_code[find]: img2_cubic[i][2][0] = color_code[replace]
    elif img2_cubic[i][2][2] == color_code[find]: img2_cubic[i][2][2] = color_code[replace]


def eliminate_duplicates(i):
    global img1_cubic, img2_cubic, change_in_img1, count

    for j in range(3):
        for k in range(3):
            if (k == 0 or k == 2):
                if (j == 0):
                    corner_count[get_color(img1_cubic[i][j][k])] += 1
                    corner_count[get_color(img2_cubic[i][j][k])] += 1
                elif (j == 2):
                    if corner_count[get_color(img1_cubic[i][j][k])] == 4:
                        img1_cubic[i][j][k] = color_code[opp_color[get_color(img1_cubic[i][j][k])]]
                    else:
                        corner_count[get_color(img1_cubic[i][j][k])] += 1
                    if corner_count[get_color(img2_cubic[i][j][k])] == 4:
                        img2_cubic[i][j][k] = color_code[opp_color[get_color(img2_cubic[i][j][k])]]
                    else:
                        corner_count[get_color(img2_cubic[i][j][k])] += 1

            if j == k == 1 and get_color(img1_cubic[i][j][k]) != opp_color[get_color(img2_cubic[i][j][k])]:
                if change_in_img1:
                    img1_cubic[i][1][1] = color_code[opp_color[get_color(img2_cubic[i][1][1])]]
                else:
                    img2_cubic[i][1][1] = color_code[opp_color[get_color(img1_cubic[i][1][1])]]
                
                change_in_img1 = not change_in_img1

            if (j == 0 and k == 1) or (j == 1 and k == 0):
                edge_count[get_color(img1_cubic[i][j][k])] += 1
                edge_count[get_color(img2_cubic[i][j][k])] += 1
            if (j == 2 and k == 1) or (j == 1 and k == 2):
                if edge_count[get_color(img1_cubic[i][j][k])] == 4:
                    img1_cubic[i][j][k] = color_code[opp_color[get_color(img1_cubic[i][j][k])]]
                else:
                    edge_count[get_color(img1_cubic[i][j][k])] += 1
                if edge_count[get_color(img2_cubic[i][j][k])] == 4:
                    img2_cubic[i][j][k] = color_code[opp_color[get_color(img2_cubic[i][j][k])]]
                else:
                    edge_count[get_color(img2_cubic[i][j][k])] += 1

    opp_check = []
    for key, val in edge_count.items():
        if val == 4:
            opp_check.append(key)

    if len(opp_check) == 2 and opp_check[0] != opp_color[opp_check[1]]:
        img1_cubic[i][0][1] =  color_code[random.choice([x for x in ["red", "orange", "white", "yellow", "green", "blue"] if x not in {opp_check[0], opp_check[1]}])]


def process_images(img1, img2):
    global img1_cubic, img2_cubic
    final_array = []
    img1_3d_to_4d = []
    img2_3d_to_4d = []

    for i in img1:
        for elem in i:
            img1_3d_to_4d.append(list(elem))
    for i in img2:
        for elem in i:
            img2_3d_to_4d.append(list(elem))

    final_array = [
        [
            [i + k + (j * (RES_W*3)) for k in range(3)] 
            for j in range(3)
        ] 
        for i in range(0, (RES_W*3)*(RES_H*3), 3)
    ]
        
    img1_cubic = [final_array[i] for i in range((RES_W*3)*RES_H) if i % (RES_W*3) < RES_W]
    temp_array = copy.deepcopy(img1_cubic)
    img2_cubic = copy.deepcopy(img1_cubic)

    for i in range(RES_H*RES_W):
        for j in range(3):
            for k in range(3):
                t1 = img1_cubic[i][j][k]   
                try:
                    img1_cubic[i][j][k] = list(img1_3d_to_4d[t1])
                    img2_cubic[i][j][k] = list(img2_3d_to_4d[t1])
                except:
                    st.error("PLease upload images with same resolution!")
                    exit(1)


    for i in range(len(img1_cubic)):

        eliminate_duplicates(i)
        clear_color_count()

        pattern_code = get_corner_code(i)
        print(pattern_code)

        if pattern_code[0] == [4,4]:
            if(pattern_code[1][0] != opp_color[pattern_code[1][1]]):
                find_and_replace(pattern_code[1][0], opp_color[pattern_code[1][0]], i)
                find_and_replace(pattern_code[1][0], opp_color[pattern_code[1][0]], i)      

        elif pattern_code[0] == [4,3,1]:
            if(pattern_code[1][1] == opp_color[pattern_code[1][0]]):
                find_and_replace(pattern_code[1][2], pattern_code[1][1], i)
            elif(pattern_code[1][1] == opp_color[pattern_code[1][2]] or pattern_code[1][0] == opp_color[pattern_code[1][2]]):
                find_and_replace(pattern_code[1][1], pattern_code[1][2], i)
            else:
                find_and_replace(pattern_code[1][1], opp_color[pattern_code[1][2]], i)

        elif pattern_code[0] == [4,2,2]: 
            if(pattern_code[1][0] != opp_color[pattern_code[1][1]] and pattern_code[1][0] != opp_color[pattern_code[1][2]] and pattern_code[1][1] != opp_color[pattern_code[1][2]]):
                find_and_replace(pattern_code[1][1], opp_color[pattern_code[1][1]], i)

        elif pattern_code[0] == [4, 2, 1, 1]:
            if(pattern_code[1][0] != opp_color[pattern_code[1][1]] and pattern_code[1][2] != opp_color[pattern_code[1][3]]):
                if(pattern_code[1][0] == opp_color[pattern_code[1][2]]):
                    find_and_replace(pattern_code[1][3], opp_color[pattern_code[1][0]], i)
                elif(pattern_code[1][0] == opp_color[pattern_code[1][3]]):
                    find_and_replace(pattern_code[1][2], opp_color[pattern_code[1][0]], i)
                elif(pattern_code[1][1] == opp_color[pattern_code[1][2]]):
                    find_and_replace(pattern_code[1][2], opp_color[pattern_code[1][3]], i)
                elif(pattern_code[1][1] == opp_color[pattern_code[1][2]]):
                    find_and_replace(pattern_code[1][3], opp_color[pattern_code[1][2]], i)

        elif pattern_code[0] == [4, 1, 1, 1, 1]:
            if(pattern_code[1][1] != opp_color[pattern_code[1][0]] and pattern_code[1][2] != opp_color[pattern_code[1][0]] and pattern_code[1][3] != opp_color[pattern_code[1][0]] and pattern_code[1][4] != opp_color[pattern_code[1][0]]):
                find_and_replace(pattern_code[1][1], opp_color[pattern_code[1][0]], i)

        elif pattern_code[0] == [3, 3, 2]:
            if(pattern_code[1][0] != opp_color[pattern_code[1][1]]):
                if pattern_code[1][0] == opp_color[pattern_code[1][2]]:
                    find_and_replace(pattern_code[1][1], pattern_code[1][2], i)
                elif pattern_code[1][1] == opp_color[pattern_code[1][2]]:
                    find_and_replace(pattern_code[1][0], pattern_code[1][2], i)
                else:
                    find_and_replace(pattern_code[1][2], random.choice([x for x in ["red", "orange", "white", "yellow", "green", "blue"] 
                                                                if x not in {pattern_code[1][0], pattern_code[1][1], pattern_code[1][2], opp_color[pattern_code[1][2]]}]), i)

        elif pattern_code[0] == [3, 3, 1, 1]:
            if(pattern_code[1][0] != opp_color[pattern_code[1][1]] and pattern_code[1][2] == opp_color[pattern_code[1][3]]): 
                find_and_replace(pattern_code[1][2], random.choice([x for x in ["red", "orange", "white", "yellow", "green", "blue"] 
                                                                if x not in {pattern_code[1][0], pattern_code[1][1], pattern_code[1][3], opp_color[pattern_code[1][3]]}]), i)

    new_img1 = [[0 for _ in range((RES_W*3))] for _ in range((RES_H*3))]
    new_img2 = [[0 for _ in range((RES_W*3))] for _ in range((RES_H*3))]

    my_1d_list = [value for dim1 in temp_array for dim2 in dim1 for value in dim2]
    new_img1_1d = [value for dim1 in img1_cubic for dim2 in dim1 for value in dim2]
    new_img2_id = [value for dim1 in img2_cubic for dim2 in dim1 for value in dim2]
    x = 0

    for i in my_1d_list:
        new_img1[i//(RES_W*3)][i%(RES_W*3)] = new_img1_1d[x]
        new_img2[i//(RES_W*3)][i%(RES_W*3)] = new_img2_id[x]
        x += 1

    new_img1 = np.array(new_img1)
    new_img2 = np.array(new_img2)
    new_img1 = new_img1.astype(np.uint8)
    new_img2 = new_img2.astype(np.uint8)

    return new_img1, new_img2

def adjust_and_crop_image(img):
    """Crop image so both width and height are multiples of 3."""
    width, height = img.size
    new_width = width - (width % 3)
    new_height = height - (height % 3)
    # Crop the image from bottom/right if necessary
    if (new_width != width) or (new_height != height):
        img = img.crop((0, 0, new_width, new_height))
    return img

def get_upscaled_images(img_array, upscale_factor, RES_H, RES_W):
    import numpy as np
    from PIL import Image

    # Repeat each input pixel to make each output pixel a square of upscale_factor × upscale_factor pixels
    upscaled_array = np.kron(img_array, np.ones((upscale_factor, upscale_factor, 1)))
    img = Image.fromarray(upscaled_array.astype('uint8'), 'RGB')

    # Calculate final upscaled shape based on RES_H, RES_W and upscale factor
    final_width = RES_W * 3 * upscale_factor
    final_height = RES_H * 3 * upscale_factor

    # This guarantees the upscaled image fills the entire mosaic grid area, regardless of aspect ratio
    return img.resize((final_width, final_height))

def main():
    st.markdown("<h1 style='text-align: center;'>Dual-Sided Rubik's Cube Mosaic</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>2.0</h1>", unsafe_allow_html=True)
    st.write("---")

    st.sidebar.image("cube.png", use_container_width=True)
    
    st.sidebar.markdown("<div style='font-size:18px; font-weight:bold;'>This application creates a dual-sided Rubik's Cube mosaic from two input images. Cubes are arranged so that flipping the grid reveals an alternate view. Ideal for installations, exhibitions, and creative visualizations. A smart integration of art, algorithms, and spatial symmetry.</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Upload Images</h3>", unsafe_allow_html=True)

    # Upload the first image
    img1 = st.file_uploader("Upload Image 1", type=["png", "jpg", "jpeg"])

    # Upload the second image
    img2 = st.file_uploader("Upload Image 2", type=["png", "jpg", "jpeg"])
    st.markdown("Generate mosaic for individual images from here (https://bestsiteever.ru/mosaic/) and drag and drop the files.")
    st.markdown("**Note: Make sure to import images with equal no. of pixels.")
    st.write("---")

    # Process the images if both are uploaded
    if img1 is not None and img2 is not None:
        global RES_H, RES_W
 
        img1 = Image.open(img1)
        img2 = ImageOps.mirror(Image.open(img2))

        img1 = adjust_and_crop_image(img1)
        img2 = adjust_and_crop_image(img2)
    
        # Optionally show user a warning if cropping occurred
        st.info(f"Images automatically cropped to {img1.size} for mosaic compatibility.")

        # img1 = img1.rotate(-90, expand=True)
        # img2 = img2.rotate(90, expand=True)

        # Convert the image to RGB format
        img1_rgb = img1.convert('RGB')
        img2_rgb = img2.convert('RGB')

        # Convert the RGB image to a NumPy array
        img1_array = np.array(img1_rgb)
        img2_array = np.array(img2_rgb)

        
        RES_H = img1_array.shape[0] // 3  # Height in cube blocks
        RES_W = img1_array.shape[1] // 3  # Width in cube blocks

        upscale_factor = 8  

        upscaled_img1 = get_upscaled_images(img1_array, upscale_factor, RES_H, RES_W)
        upscaled_img2 = get_upscaled_images(img2_array, upscale_factor, RES_H, RES_W)

        st.subheader("Image 1")
        st.image(upscaled_img1, use_container_width=True)

        st.subheader("Image 2")
        st.image(upscaled_img2, use_container_width=True)

        if st.button("Process Images"):

            new_img1, new_img2 = process_images(img1_array, img2_array)

            upscale_factor = 8  

            upscaled_img1 = get_upscaled_images(new_img1, upscale_factor, RES_H, RES_W)
            upscaled_img2 = get_upscaled_images(new_img2, upscale_factor, RES_H, RES_W)

            st.subheader("Converted Image 1")
            st.image(upscaled_img1, use_container_width=True)

            st.subheader("Converted Image 2")
            st.image(upscaled_img2, use_container_width=True)

            st.success("Images processed successfully!")
            
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
                for image, filename in zip([Image.fromarray(new_img1), Image.fromarray(new_img2)], ['miniature_img1.png', 'miniature_img2.png']):
                    # Create an in-memory stream for each image
                    image_stream = BytesIO()
                    image.save(image_stream, format='PNG')
                    image_bytes = image_stream.getvalue()
                    # Add the image bytes to the ZIP file
                    zip_file.writestr(filename, image_bytes)

            # Provide the ZIP file for download
            zip_data = zip_buffer.getvalue()
            st.download_button(
                label="Download Images",
                data=zip_data,
                file_name="DualSided_Rubik'sCube_images.zip",
                mime="application/zip",
            )
            st.markdown("Paste the (downloaded)converted images for making mosaic here (https://bestsiteever.ru/mosaic/) and download the pdf.")
        

if __name__ == "__main__":
    main()
