from setuptools import setup, find_packages

from BreachCompilationRestAPI import __version__, __author__, __email__, __license__

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", encoding='utf-8') as f:
    readme = f.read()

with open("CHANGELOG.rst") as f:
    changelog = f.read()

setup(
    name="BreachCompilationRestAPI",
    version=__version__,
    description="Rest API for the BreachCompilation collection",
    long_description=readme + "\n\n" + changelog,
    long_description_content_type='text/markdown',
    license=__license__,
    author=__author__,
    author_email=__email__,
    url="https://github.com/bierschi/BreachCompilationRestAPI",
    packages=find_packages(),
    data_files=[
        ('/etc/systemd/system', ['service/BreachCompilationApp.service'])
    ],
    package_data={'BreachCompilationRestAPI': ['config/*']},
    install_requires=required,
    keywords=["BreachCompilation", "credentials", "leaked", "REST API"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: Name Service (DNS)",
    ],
    entry_points={
        "console_scripts": [
            'BreachCompilationApp = BreachCompilationRestAPI.app:main'
        ],
    },
    zip_safe=False,
)
