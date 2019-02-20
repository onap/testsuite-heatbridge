from setuptools import setup

setup(
    name='${PROJECT_NAME}',  # This is the name of your PyPI-package.
    version='${VERSION}',  # Update the version number for new releases
    description='Script to input heat stack information into aai',
    install_requires=['python-novaclient', 'python-cinderclient',
                      'python-glanceclient', 'os_client_config',
                      'python-neutronclient', 'python-heatclient'],
    packages=['heatbridge'],  # The name of your scipts package
    package_dir={'heatbridge': 'heatbridge'}  # Location of the scripts package
)
