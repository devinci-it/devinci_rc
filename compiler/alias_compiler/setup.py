from setuptools import setup, find_packages

setup(
    name='alias_generator',
    version='1.0.0',
    description='A utility for compiling alias definitions and generating alias scripts',
    author='devinci-it',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'alias-generator=alias_generator.main:main',
            'generate-bash-function=alias_generator.generate_bash_function:main',
            'parse-positional-args=alias_generator.parse_positional_args:main',
        ],
    },
    install_requires=[
        # Add any dependencies here if needed
    ],
)
