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
    description="A tool for extracting context around keywords in conversation text files",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
