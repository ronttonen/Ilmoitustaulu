from setuptools import setup

setup(
	name='ilmoitustaulu',
	packages=['ilmoitustaulu'],
	include_package_data=True,
	install_requires=[
		'flask','flask-login','flask-sqlalchemy','pymysql',
	],
)