from setuptools import setup, find_packages

setup(
    name='skillcornerviz',
    version='1.0.9',

    url='https://github.com/liamMichaelBailey/skillcornerviz',
    author='Liam Michael Bailey',
    author_email='liam.bailey@skillcorner.com',

    packages=find_packages(include=['skillcornerviz', 'skillcornerviz.*']),

    package_data={'skillcornerviz': ['resources/Roboto/Roboto-Black.ttf',
                                     'resources/Roboto/Roboto-BlackItalic.ttf',
                                     'resources/Roboto/Roboto-Bold.ttf',
                                     'resources/Roboto/Roboto-BoldItalic.ttf',
                                     'resources/Roboto/Roboto-Italic.ttf',
                                     'resources/Roboto/Roboto-Light.ttf',
                                     'resources/Roboto/Roboto-LightItalic.ttf',
                                     'resources/Roboto/Roboto-Medium.ttf',
                                     'resources/Roboto/Roboto-MediumItalic.ttf',
                                     'resources/Roboto/Roboto-Regular.ttf',
                                     'resources/Roboto/Roboto-Thin.ttf',
                                     'resources/Roboto/Roboto-ThinItalic.ttf']},

    install_requires=['adjustText>=0.7.3',
                      'matplotlib>=3.7.2',
                      'numpy>=1.24.2',
                      'pandas>=1.5.3',
                      'seaborn>=0.11.2',
                      'setuptools>=65.0.0'],

    include_package_data=True,
)
