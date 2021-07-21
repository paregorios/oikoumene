import setuptools
from pip._vendor.packaging.version import Version

with open("README.md", "r") as fh:
    long_description = fh.read()

# Get the version from the oikoumene module.
oikoumene_version = None
with open('oikoumene/__init__.py', 'r') as fp:
    for line in fp:
        if line.startswith("__version__"):
            oikoumene_version = Version(
                line.split("=")[1].strip().strip("\"'"))
            break

if not oikoumene_version:
    raise ValueError("Could not determine Oikoumene's version")
    
setuptools.setup(
    name="oikoumene",
    version=oikoumene_version,
    author="Tom Elliott",
    author_email="tom.elliott@nyu.edu",
    description="gazetteer tools",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['airtight', 'python-slugify', 'textnorm'],
    python_requires='>=3.9.6'
)
