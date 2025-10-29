from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
with open("backend/requirements.txt") as f:
    requirements = f.read().splitlines()

# Find all packages under the backend directory
packages = find_packages(where='backend')

setup(
    name="student_planner",
    version="1.0.0",
    packages=[f"backend.{pkg}" for pkg in packages],
    package_dir={"": "."},
    install_requires=requirements,
    python_requires=">=3.8",
    include_package_data=True,
)
