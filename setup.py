from setuptools import setup, find_packages

setup(
    name='pyFormal',
    version='0.1.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyperclip',
        'matplotlib',
        'numpy',
        'click',
        'Pillow',  # Note: This is actually "Pillow" on PyPI
        'pillow_heif',
    ],
    entry_points={
        'console_scripts': [
            'pyFormal=pyFormal.images2grid:main',
        ],
    },
    author='Malek',
    author_email='shmeek8@gmail.com',
    description='An application to create a grid of nicely formatted images from a folder of images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/malekinho8/pyFormal',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)