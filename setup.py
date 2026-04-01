from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mahounou-uconv",
    version="0.2.0",
    description="Lightweight unit converter library with support for 13 unit categories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mahounou Dev Team",
    author_email="",
    url="https://github.com/ksnjkdppdojdim-star/UconvPy",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'uconvpy=uconv.cli:main',
        ],
    },
    extras_require={
        'dev': ['pytest>=7.0', 'pytest-cov>=3.0']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="units converter measurement distance weight time currency temperature speed area volume energy pressure power data",
    project_urls={
        "Bug Reports": "https://github.com/ksnjkdppdojdim-star/UconvPy/issues",
        "Source": "https://github.com/ksnjkdppdojdim-star/UconvPy",
    },
)
