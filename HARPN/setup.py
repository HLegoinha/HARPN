import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HARPN_explorer", # Replace with your own username
    version="0.0.1",
    author="Henrique Legoinha",
    author_email="up201505577@fc.up.pt",
    description="A package that allows searching and downloading line spectra from the HARPN database",
    url="https://github.com/HLegoinha/HARPN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows Linux",
    ],
    python_requires='>=3.7',
)