# This function should take in a folder path (string) and print the saved image path as well as save the image to the clipboard

# Importing libraries
import os
import pyperclip
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import subprocess
import numpy as np
import click
from matplotlib import gridspec
from PIL import Image, ImageFilter, ImageChops, ImageDraw
from pillow_heif import register_heif_opener
from time import time

# Set verbosity
verbosity = 'show_plots'

# use latex for matplotlib
plt.rc('text', usetex=True)

# Register the HEIF file format with Pillow
register_heif_opener()


# Use the click.command() and click.argument() decorators
@click.command()
@click.argument('folder_path')
@click.argument('save_folder_path', default='./saved-images')
def main(folder_path, save_folder_path='./saved-images'):
    # Get the image paths
    image_paths = get_image_paths(folder_path)

    # plot the images
    good_image_path = plot_images(image_paths, save_folder_path)

    # load the image
    img = Image.open(good_image_path)

    # save the image to the clipboard
    send_img_to_clipboard(good_image_path)

def send_img_to_clipboard(image_path):
    # Use the 'pbcopy' command to set the clipboard data
    subprocess.run(["osascript", "-e", f'set the clipboard to (read (POSIX file "{image_path}") as JPEG picture)'])

# Function to get the image paths
def get_image_paths(folder_path):
    # Get the image paths
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith('.HEIC'):
            image_paths.append(os.path.join(folder_path, filename))
    
    print(f'Found {len(image_paths)} images in {folder_path}')
    return image_paths

def process_image(img):
    width, height = img.size
    if width > height:
        img = img.crop(((width - height) / 2, 0, (width + height) / 2, height))
    else:
        img = img.crop((0, (height - width) / 2, width, (height + width) / 2))
    
    # Create a blurred version of the image
    blurred = img.filter(ImageFilter.GaussianBlur(radius=5))  # Adjust radius as needed
    
    # Create a mask: white circle in the middle, black outside
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((width*0.1, height*0.1, width*0.9, height*0.9), fill=255)

    mask = mask.convert("RGB")  # Convert the mask to RGB mode
    mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=100))  # Apply a blur to the mask
    
    # Blend original image and blurred image using mask
    img = ImageChops.darker(img, ImageChops.lighter(blurred, mask_blurred))

    return img

# Function to plot the images in a 2-row grid if there are 4, 6, 8 images, and if there are 2 or 3 images, plot them in a row side by side. If there are 5 or 7 images, the first 3 should be plotted in a row and the last 2 should be plotted in a row below and the 6th position should be empty. If there are 7 images, apply a similar logic and plot the images in a grid with 2 rows. If there are 9 images, plot the images in 3 rows. If there are 10 images, plot them in 2 rows.
# The images should also be clipped to be square about the center of the image and all have the same aspect ratio.
# The function should take in a list of image paths and a save folder path and save the image to the save folder path and return the saved image path. It should use the current time to create the name of the saved file.
def plot_images(image_paths, save_folder_path='./saved-images'):
    num_images = len(image_paths)
    timestamp_tag = f'{time()}'[:-5]
    save_path = os.path.join(save_folder_path, f'images-{timestamp_tag}.jpg')
    
    assert num_images > 1 and num_images <= 10, 'Number of images must be between 2 and 10!'
    assert os.path.exists(save_folder_path), 'Save folder path does not exist!'
    
    if num_images == 2 or num_images == 3:
        fig, ax = plt.subplots(1, num_images, figsize=(10, 10))

        for i in range(num_images):
            img = Image.open(image_paths[i])
            width, height = img.size
            if width > height:
                img = img.crop(((width - height) / 2, 0, (width + height) / 2, height))
            else:
                img = img.crop((0, (height - width) / 2, width, (height + width) / 2))

            ax[i].imshow(img)
            ax[i].axis('off')
            
            # Add annotation
            annotation = chr(97 + i)  # Get the corresponding letter (a, b, c, etc.)
            box_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E0E0E0', alpha=0.8)
            ax[i].text(0.95, 0.95, f'$\mathrm{{({annotation})}}$', transform=ax[i].transAxes,
                       fontsize=14, verticalalignment='top', horizontalalignment='right',
                       bbox=box_props)

        plt.subplots_adjust(wspace=0, hspace=0)
        fig.tight_layout(pad=0)
        plt.axis('off')
        if verbosity == 'show_plots':
            plt.show()
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0)
    elif num_images >= 4 and num_images <= 8:
        nrows = 2
        ncols = int(np.ceil(num_images / 2))

        fig = plt.figure(figsize=(5 * ncols, 10))  # Adjusted figure size

        gs = gridspec.GridSpec(nrows, ncols,
                            width_ratios=[1] * ncols,
                            height_ratios=[1] * nrows,
                            wspace=0,
                            hspace=0)

        for i in range(num_images):
            img = Image.open(image_paths[i])

            # process the image
            img = process_image(img)  
      
            ax = plt.subplot(gs[i])
            ax.imshow(img, aspect='auto')
            ax.axis('off')

            # Add annotation
            annotation = chr(97 + i)
            box_props = dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E0E0E0', alpha=0.8)
            ax.text(0.95, 0.95, f'$\mathrm{{({annotation})}}$', transform=ax.transAxes,
                    fontsize=14, verticalalignment='top', horizontalalignment='right',
                    bbox=box_props)

        plt.axis('off')
        if verbosity == 'show_plots':
            plt.show()
        fig.tight_layout(pad=0)
        fig.savefig(save_path, bbox_inches='tight', pad_inches=0)


    
    return save_path

if __name__ == '__main__':
    main()
            