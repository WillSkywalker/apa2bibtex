from setuptools import setup, find_packages

setup(
    name="apa2bibtex",
    version="0.0.1",
    packages=find_packages(exclude=['tests*']),

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.md', '*.rst'],
    },

    # metadata for upload to PyPI
    author="Will Skywalker",
    author_email="cxbats@gmail.com",
    description="A command tool to covert APA references to .bibtex format.",
    license="Apache 2.0",
    url="https://github.com/WillSkywalker/apa2bibtex",   # project home page, if any
    keywords='apa bibtex tex latex reference academic',

    entry_points={
        'console_scripts': [
            'apa2bibtex = apa2bibtex.apa2bibtex:main',
        ],
    },
    install_requires=[
        'bs4',
        'requests',
    ],

    # could also include long_description, download_url, classifiers, etc.
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
