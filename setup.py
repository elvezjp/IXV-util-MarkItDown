from setuptools import setup, find_packages

# バージョンをpyproject.tomlから読み取るか、
# または__about__.pyから読み取る
try:
    from markitdown import __version__
except ImportError:
    __version__ = '0.1.0'

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
    author='Elvez, Inc.',
    license='MIT',
    python_requires='>=3.8',
)
