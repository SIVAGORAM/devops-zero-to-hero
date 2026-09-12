from setuptools import setup, find_packages

setup(
    name="devops-toolkit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "PyYAML",
        "python-dotenv",
        "boto3",
        "Flask"
    ],
    entry_points={
        "console_scripts": [
            "devops-tool=main:main"
        ]
    }
)
