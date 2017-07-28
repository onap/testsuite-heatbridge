from setuptools import setup

setup(
    name='heatbridge',            # This is the name of your PyPI-package.
    version='0.2',                          # Update the version number for new releases     
    description='Script to input heat stack information into aai',    # Info about script
    install_requires=['python-novaclient','python-cinderclient','python-glanceclient', 'os_client_config', 'python-neutronclient', 'python-heatclient'], # what we need
    packages=['heatbridge'],       # The name of your scipts package
    package_dir={'heatbridge': 'heatbridge'} # The location of your scipts package
)