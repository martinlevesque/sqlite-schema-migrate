from setuptools import setup, find_packages

setup(
    name="sqlite-schema-migration",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sqlite_schema_migration=src.main:main',
        ],
    },
)