from setuptools import setup, find_packages
from markitdown import __version__

setup(
    name='IXV-util-MarkItDown',
    version=__version__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'markitdown=markitdown.cli:main'
        ]
    },
    description='Simple docx to Markdown converter',
    author='IXV Team',
    license='MIT'
)
