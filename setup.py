import setuptools

setuptools.setup(
    name="portainer_management",
    version="0.1.4",
    author="Florian Gottwalt",
    author_email="f.gottwalt@unsw.edu.au",
    description="Portainer Mangement Scripts",
    packages=setuptools.find_packages(),
    install_requires=[
    'portainer_api',
    'PyYAML'
    ],
    dependency_links=[
        'https://pypi.python.org/simple'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
