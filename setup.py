from setuptools import setup, find_packages

setup(
    name="topic-matcher",
    version="0.1.0",
    description="",
    author="",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",,
    ],
    entry_points={
        "console_scripts": [
            "topic-matcher=app:main"
        ],
    },
)