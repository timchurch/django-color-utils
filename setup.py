from setuptools import setup, find_packages

setup(
    name='django-color-utils',
    version='0.1.0',
    description='Collection of color picker widgets and color database model fields for Django.',
    long_description=open('README.md').read(),
    author='Tim Church',
    url='hhttps://github.com/timchurch/django-color-utils',
    include_package_data=True,
    package_data={'': ['README.md']},
    packages=['color_utils']
)
