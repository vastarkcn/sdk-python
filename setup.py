from setuptools import setup, find_packages

setup(
    name="vastark-recaptcha",
    version="1.0.0",
    description="vastark recaptcha Python SDK",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="vastark",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.8",
    install_requires=[
        "urllib3>=1.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
