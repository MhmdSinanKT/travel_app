from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in travel_app/__init__.py
from travel_app import __version__ as version

setup(
	name="travel_app",
	version=version,
	description="A Travel app fr booking vehicles and seats in vehicles",
	author="Muhammed Sinan K T",
	author_email="sinan@travel.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
