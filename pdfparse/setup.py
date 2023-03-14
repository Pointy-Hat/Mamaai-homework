from setuptools import find_packages, setup

setup(
    name="pdfparse-server",
    version="1.0",
    scripts=find_packages(),
    install_requires=["flask", "pdfminer.six"],
)
