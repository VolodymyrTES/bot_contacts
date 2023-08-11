from setuptools import setup, find_namespace_packages

setup(
    name='bot_contacts',
    version='1',
    description='bot',
    url='https://github.com/VolodymyrTES',
    author='Volodymyr Kyryienko',
    author_email='v.kyryienko856790@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['bot-contacts = bot_contacts.main:main']}
)