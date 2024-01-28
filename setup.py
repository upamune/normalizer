from setuptools import setup

setup(
    name='lufs-normalizer',
    version='0.1.0',
    packages=["normalizer"],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            "lufs-normalizer=normalizer.cli:main"
        ]
    }
)
