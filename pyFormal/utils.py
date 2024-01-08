import os
import pyperclip
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import subprocess
import numpy as np
import click
from matplotlib import gridspec
from PIL import Image, ImageFilter, ImageOps, ImageDraw
from pillow_heif import register_heif_opener
from time import time

# Set verbosity
verbosity = 'show_plots'

def round_mp4_corners_with_mask(file_path, rounded_corner_size,rounded_corner_pct):
    # Convert shadow_radius from pt to pixels (assuming 1pt = 1.3333 pixels, but this may vary)
    radius_in_pixels = int(rounded_corner_size * 1.3333)

    # Use ffmpeg to generate the mask with rounded corners
    mask_path = "mask.png"
    subprocess.call([
        'ffmpeg', '-y', '-f', 'lavfi', '-i',
        f'color=c=white:s=1280x720:duration=0.1,drawbox=w=iw:h=ih:t={radius_in_pixels}:color=black@1.0',
        '-frames:v', '1',
        mask_path
    ])

    output_path = file_path.replace('.mp4','-rounded.mp4')

    # Overlay the mask onto the video
    subprocess.call([
        'ffmpeg', '-y', '-i', file_path, '-i', mask_path, '-filter_complex',
        '[0][1]overlay=format=auto',
        output_path
    ])

    return output_path

def round_mp4_corners(file_path,rounded_corner_size,rounded_corner_pct):


    return None # should use ffmpeg to save the 

def make_fancy_figure_for_odd_n(n, image_paths, border_width_ratio, blur_intensity, border_color, label_font_size, box_props, mode, nrows=2):
    """
    Creates fancy figure for n images if n is odd.
    """
    # We need to determine the number of columns based on n
    cols = n + 1

    # define desired ncols
    ncols = int(np.ceil(n / nrows))

    # specify the subplot size
    subplot_size = 3

    # initialize the figure and gridspec
    fig = plt.figure(figsize=(subplot_size * ncols, subplot_size * nrows))  # Adjusted figure size
    gs = gridspec.GridSpec(nrows, cols,
                        width_ratios=[1] * cols,
                        height_ratios=[1] * nrows,
                        wspace=0,
                        hspace=0)

    # initialize an image counter
    d = 0

    # For the top row, we need each guy to take up two spaces
    for i in range(nrows): # iterate over rows. Currently this implementation only works for 2 rows.
        # initialize the column counter
        c = 0 if i == 0 else 1
        while c < cols:
            print(f'i: {i}, c: {c}, image: {d}')
            img = Image.open(image_paths[d])
        
            # process the image
            img = process_image(img, border_width_ratio, blur_intensity, border_color, mode)  

            ax = plt.subplot(gs[i,c:c+2])
            ax.imshow(img, aspect='auto')
            ax.axis('off')

            # Add annotation
            annotation = chr(97 + d)
            ax.text(0.95, 0.95, f'$\mathrm{{({annotation})}}$', transform=ax.transAxes,
                    fontsize=label_font_size, verticalalignment='top', horizontalalignment='right',
                    bbox=box_props)

            c += 2
            d += 1
            if (c+2) >= cols and i == 1:
                break
    
    return fig
            
def process_image(img, border_width_ratio=0.05, blur_intensity=10, border_color="white", mode="crop"):  # Changed border_width to border_width_ratio
    # Cropping logic 
    width, height = img.size
    max_size = max(width, height)

    if mode == 'crop':
        if width > height:
            img = img.crop(((width - height) / 2, 0, (width + height) / 2, height))
        else:
            img = img.crop((0, (height - width) / 2, width, (height + width) / 2))
    elif mode == 'pad':
        new_img = Image.new('RGB', (max_size, max_size), border_color)
        offset = ((max_size - width) // 2, (max_size - height) // 2)
        new_img.paste(img, offset)
        img = new_img
    else:
        raise NotImplementedError('Mode must be either "crop" or "pad".')

    # Determine border width based on image size
    border_width = int(max(img.width, img.height) * border_width_ratio)

    print(f'Image size: {img.size}')
    print(f'Boder width: {border_width}')

    # Create a new image with borders (total image size = original image size + 2*border width)
    total_width = img.width + 2 * border_width
    total_height = img.height + 2 * border_width
    img_with_border = Image.new('RGB', (total_width, total_height), border_color)  # Create a new white image

    # Paste original image at the center of this new image
    img_with_border.paste(img, (border_width, border_width))

    # Create a copy of our new image and apply the blur filter to it
    blurred_img_with_border = img_with_border.copy().filter(ImageFilter.GaussianBlur(radius=blur_intensity))

    # Create a mask that is true for the border region and false for the inner region
    mask = Image.new('L', (total_width, total_height), 0)  # Create a new black image
    ImageDraw.Draw(mask).rectangle([border_width, border_width, total_width - border_width, total_height - border_width], fill=255)

    # Combine the blurred and non-blurred images using the mask
    final_img = Image.composite(img_with_border, blurred_img_with_border, mask)
    return final_img


def send_img_to_clipboard(image_path):
    # Use the 'pbcopy' command to set the clipboard data
    subprocess.run(["osascript", "-e", f'set the clipboard to (read (POSIX file "{image_path}") as JPEG picture)'])

# Function to get the image paths
def get_image_paths(folder_path):
    # Get the image paths
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".PNG") or filename.endswith(".JPG") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith('.HEIC') or filename.endswith('.heic'):
            image_paths.append(os.path.join(folder_path, filename))
    
    print(f'Found {len(image_paths)} images in {folder_path}')

    # order the paths by the time they were created
    image_paths = sorted(image_paths, key=lambda path: os.path.basename(path).lower())
    
    return image_paths

# Function to plot the images in a 2-row grid if there are 4, 6, 8 images, and if there are 2 or 3 images, plot them in a row side by side. If there are 5 or 7 images, the first 3 should be plotted in a row and the last 2 should be plotted in a row below and the 6th position should be empty. If there are 7 images, apply a similar logic and plot the images in a grid with 2 rows. If there are 9 images, plot the images in 3 rows. If there are 10 images, plot them in 2 rows.
# The images should also be clipped to be square about the center of the image and all have the same aspect ratio.
# The function should take in a list of image paths and a save folder path and save the image to the save folder path and return the saved image path. It should use the current time to create the name of the saved file.
def plot_images(image_paths, save_folder_path='./saved-images', save_name=None, label_font_size=20, border_width_ratio=0.05, blur_intensity=10, border_color='white', mode="crop"):
    num_images = len(image_paths)
    timestamp_tag = f'{time()}'[:-5]
    save_path = os.path.join(save_folder_path, f'images-{timestamp_tag}.jpg') if save_name is None else os.path.join(save_folder_path, save_name)

    # Check if the save folder exists and create it if not
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)
    
    assert num_images > 1 and num_images <= 10, 'Number of images must be between 2 and 10!'

    # define the box properties
    box_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E0E0E0', alpha=0.8)
    
    if num_images == 2 or num_images == 3:
        fig, ax = plt.subplots(1, num_images, figsize=(10, 10))

        for i in range(num_images):
            img = Image.open(image_paths[i])
            img = process_image(img, border_width_ratio, blur_intensity, border_color, mode)

            ax[i].imshow(img)
            ax[i].axis('off')
            
            # Add annotation
            annotation = chr(97 + i)  # Get the corresponding letter (a, b, c, etc.)
            ax[i].text(0.95, 0.95, f'$\mathrm{{({annotation})}}$', transform=ax[i].transAxes,
                       fontsize=label_font_size, verticalalignment='top', horizontalalignment='right',
                       bbox=box_props)

        plt.subplots_adjust(wspace=0, hspace=0)
        fig.tight_layout(pad=0)
        plt.axis('off')
        if verbosity == 'show_plots':
            plt.show()
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=600)
    elif num_images in {4, 6, 8}:  # 4, 6, 8 images
        nrows = 2
        ncols = int(np.ceil(num_images / 2))

        # Set the size of an individual subplot, keeping them the same for a 1:1 aspect ratio
        subplot_size = 3

        # Set the figure size based on the subplot size and number of rows and columns
        fig = plt.figure(figsize=(subplot_size * ncols, subplot_size * nrows))

        gs = gridspec.GridSpec(nrows, ncols,
                            width_ratios=[1] * ncols,
                            height_ratios=[1] * nrows,
                            wspace=0,
                            hspace=0)

        for i in range(num_images):
            img = Image.open(image_paths[i])

            # process the image
            img = process_image(img, border_width_ratio, blur_intensity, border_color, mode)      
            ax = plt.subplot(gs[i])
            ax.imshow(img, aspect='auto')
            ax.axis('off')

            # Add annotation
            annotation = chr(97 + i)
            ax.text(0.95, 0.95, f'$\mathrm{{({annotation})}}$', transform=ax.transAxes,
                    fontsize=label_font_size, verticalalignment='top', horizontalalignment='right',
                    bbox=box_props)
        
        plt.axis('off')
        if verbosity == 'show_plots':
            plt.show()
        fig.tight_layout(pad=0)
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=600)
    elif num_images in {5,7,9}: # odd number of images
        fig = make_fancy_figure_for_odd_n(num_images, image_paths, border_width_ratio, blur_intensity, border_color, label_font_size, box_props, mode)
        plt.axis('off')
        if verbosity == 'show_plots':
            plt.show()
        fig.tight_layout(pad=0)
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=600)
    
    return save_path
