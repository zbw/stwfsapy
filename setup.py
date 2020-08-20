import pathlib
from setuptools import setup, find_packages

# The directory containing this file
file_dir = pathlib.Path(__file__).parent

# The text of the README file
readme_txt = (file_dir / "Readme.md").read_text()

setup(
    name="stwfsapy",
    version="0.01.2",
    description="A library for match labels of thesaurus concepts to text" + (
        " and assigning scores to found occurrences."),
    long_description=readme_txt,
    long_description_content_type="text/markdown",
    url="https://github.com/zbw/stwfsapy",
    author="Moritz Fuerneisen",
    author_email="m.fuerneisen@zbw.eu",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["rdflib==4.2.*", "scikit-learn==0.22.*"],
    tests_require=['py', 'pytest', 'pytest-mock'],
    extras_require={
        'dev': [
            "pytest==5.4.*",
            "pytest-mock==1.7.*",
            "pytest-pycodestyle==2.2.*",
            "pytest-cov==2.8.*",
            "codecov==2.1.*",
            ]
        },
    python_requires='>=3.6',
)
