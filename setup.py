import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upskills.email_classification",
    version="0.0.1",
    author="AB",
    author_email="aurelien.baelde@upskills.ai",
    description="email classification project",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/upskills-paris-mllab/email_classification",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :",
        "Operating System :: OS Independent",
    ],
)