from distutils.core import setup

setup(
    # Application name:
    name="DroidAgile",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="name surname",
    author_email="name@addr.ess",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="DroidAgile",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask", "pygame"
    ],
)