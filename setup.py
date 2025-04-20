from setuptools import setup, find_packages

setup(
    name="conversation-extractor",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'conversation-extractor=conversation_extractor.cli:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        'nltk>=3.6.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-html>=3.0.0',
        ],
    },
    description="A tool for extracting context around keywords in conversation text files",
    author="Shaun Jackson",
    author_email="washyu@hotmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
