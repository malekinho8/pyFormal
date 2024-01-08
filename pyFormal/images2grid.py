# This function should take in a folder path (string) and print the saved image path as well as save the image to the clipboard

# Importing libraries
import pyperclip
import matplotlib.pyplot as plt
import click
import sys; sys.path.append('./')
from pillow_heif import register_heif_opener
from pyFormal.utils import *

# use latex for matplotlib
plt.rc('text', usetex=True)

# Register the HEIF file format with Pillow
register_heif_opener()


# Use the click.command() and click.argument() decorators
@click.command()
# add a click argument for the label box size
@click.option('--label_font_size','-l', default=18, help='Font size for the image labels')
@click.option('--use_clipboard_for_folder_path','-c', default=True, help='Use the clipboard for the folder path')
@click.option('--save_folder_path', '-f', default='./pyFormal-figures', help='Folder path to save the images')
@click.option('--border_width_ratio', '-b', type=float, default=0.01, help='How much to make the border width of the output image')  # Change from 'border_width' to 'border_width_ratio'
@click.option('--blur_intensity','-i', type=int, default=10, help='How intense to make the border width blur.') # New argument for blur intensity
@click.option('--manual_image_folder_path', '-m', default=None, help='Manually enter the image folder path. To use this, use_clipboard_for_folder_path must be set to False.')
@click.option('--border-color', '-bc', default='white', help='Color of the border.')
@click.option('--resize-mode', '-r', default='crop', help='Mode for resizing the images. Options are "crop" and "pad".')

def main(label_font_size, use_clipboard_for_folder_path, save_folder_path, border_width_ratio, blur_intensity, manual_image_folder_path, border_color, resize_mode):  # Include blur_intensity in function arguments
    if not use_clipboard_for_folder_path:
        # Get the folder path
        folder_path = input('Enter the folder path: ')
    else:
        # Get the folder path from the clipboard
        if manual_image_folder_path is None:
            folder_path = pyperclip.paste()
        else:
            folder_path = manual_image_folder_path

    # Get the image paths
    image_paths = get_image_paths(folder_path)

    # plot the images
    good_image_path = plot_images(image_paths, save_folder_path, None, label_font_size, border_width_ratio, blur_intensity, border_color, resize_mode)

    # load the image
    img = Image.open(good_image_path)

    # save the image to the clipboard
    send_img_to_clipboard(good_image_path)

if __name__ == '__main__':
    main()
            