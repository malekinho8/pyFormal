# This function should take in an mp4 video file and make all of the frames have nice rounded  corners with a transparent bakcground


import click
import pyperclip
import sys; sys.path.append('./')
from pyFormal.utils import round_mp4_corners_with_mask

@click.command()

@click.option('--use_clipboard_for_mp4_path','-c', default=True, help='Use the clipboard for the folder path')
@click.option('--mp4-path','-m',default=None, help='MP4 full file path (optional).')
@click.option('--rounded-corner-size','-r',default=6,help='Pixel size of the radius of the rounded corner in each frame.')
@click.option('--rounded-corner-pct','-p',default=0.8,help='How much to scale the pixel size when calculating the true rounded radius to use.')

def main(use_clipboard_for_mp4_path, mp4_path, rounded_corner_size, rounded_corner_pct):

    if not use_clipboard_for_mp4_path:
        # Get the folder path
        file_path = input('Enter the folder path: ')
    else:
        # Get the folder path from the clipboard
        if mp4_path is None:
            file_path = pyperclip.paste()
        else:
            file_path = mp4_path
        
    round_mp4_corners_with_mask(file_path,rounded_corner_size,rounded_corner_pct)

    # should use ffmpeg to save the 
    return None


if __name__ == '__main__':
    main()