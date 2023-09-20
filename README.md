# pyFormal

**pyFormal** is a tool for creating formal figures of grids of images in Python. This tool allows users to take a folder of images and transform them into a neatly formatted grid with desired parameters such as label font size, border width, blur intensity, and more.

## Prerequisites

Before you can use **pyFormal**, you need to install a LaTeX distribution:

- For macOS users: Install [MacTeX](http://www.tug.org/mactex/).
  
  ```bash
  brew install --cask mactex-no-gui
  ```

- For Windows users: Install [MiKTeX](https://miktex.org/download).

- For Linux users: Most distributions have TeX Live in their repositories. For example, on Debian/Ubuntu:

  ```bash
  sudo apt-get install texlive-full
  ```

## Installation

Once the prerequisites are installed, you can install **pyFormal** via pip:

```bash
pip install pyFormal
```

## Usage

To use **pyFormal**, navigate to the directory containing your images and run the following command:

```bash
pyFormal --label_font_size <FONT_SIZE> --use_clipboard_for_folder_path <TRUE/FALSE> --save_folder_path <FOLDER_PATH> --border_width_ratio <BORDER_RATIO> --blur_intensity <BLUR_INTENSITY> --manual_image_folder_path <MANUAL_PATH> --border-color <BORDER_COLOR> --resize-mode <RESIZE_MODE>
```

### Options:

- `--label_font_size, -l`: Font size for the image labels (default: 18).
- `--use_clipboard_for_folder_path, -c`: Use the clipboard for the folder path (default: True).
- `--save_folder_path, -f`: Folder path to save the images (default: './pyFormal-figures').
- `--border_width_ratio, -b`: How much to make the border width of the output image (default: 0.01).
- `--blur_intensity, -i`: How intense to make the border width blur (default: 10).
- `--manual_image_folder_path, -m`: Manually enter the image folder path. To use this, use_clipboard_for_folder_path must be set to False (default: None).
- `--border-color, -bc`: Color of the border (default: 'white').
- `--resize-mode, -r`: Mode for resizing the images. Options are "crop" and "pad" (default: 'crop').

### Example 1: Using Clipboard Path

If you've copied the path to your folder (e.g., `C:\Users\Username\Documents\my_images`) to your clipboard, you can utilize the clipboard to fetch the path directly and run the command simply with all of the default settings like so:

```bash
pyFormal
```

By default, **pyFormal** will try to use the folder path from the clipboard if the `--use_clipboard_for_folder_path` option is not set to `False`. In this example, the application will fetch the path from your clipboard, create a grid of images, and save the output in the `pyFormal-figures` folder using the default settings. Furthermore, once you close the figure preview window, it will copy the image data to your clipboard so it can be pasted easily into whatever document you are working on.

### Example 2: Specifying the Image Folder in the Command Line

Assuming you have a folder named `my_images` and you want to save the grid to a folder named `output`, you would run:

```bash
pyFormal -c False -m ./my_images
```

This will create a grid of images from the `my_images` folder and save the output in the `pyFormal-figures` folder using the default settings.

## Contributing

If you find any issues or have suggestions, please open an issue!