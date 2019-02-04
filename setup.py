import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-easypay",
    version="0.1.0",
    author="Dario Marcelino",
    author_email="dario@appscot.com",
    install_requires=[
        'Django>=1.10',
        'requests>=2.18.4',
    ],
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
