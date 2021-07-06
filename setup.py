import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="blunder_wunder",
    version="0.0.1",
    author="Edmund Martin",
    description="Bulk analyse Chess games using a UCI engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EdmundMartin/blunder_wunder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "blunder_wunder"},
    packages=setuptools.find_packages(where="blunder_wunder"),
    python_requires=">=3.8",
)
