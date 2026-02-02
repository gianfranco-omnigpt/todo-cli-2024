"""Setup configuration for CLI ToDo App."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="todo-cli",
    version="1.0.0",
    author="CLI ToDo App Team",
    description="A minimal command-line application for managing personal tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gianfranco-omnigpt/todo-cli-2024",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "todo=todo.__main__:main",
        ],
    },
)
