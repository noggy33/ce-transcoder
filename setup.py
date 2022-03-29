from setuptools import setup, find_packages

setup(
    name='app',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ibm-cos-sdk',
        'ffmpeg-python'
    ],
    entry_points='''
        [console_scripts]
        app=app
    ''',
)