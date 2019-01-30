import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-easypay",
    version="0.0.1",
    author="Dario Marcelino",
    author_email="dario@appscot.com",
    description="A Django package for Easypay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmarcelino/django-easypay",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

