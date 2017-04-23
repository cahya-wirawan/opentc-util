from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()

__version__ = ""
exec(open('opentc/util/setting.py').read())

setup(
    name='opentc-util',
    version=__version__,
    description='The util package of OpenTC (A text classification engine using machine learning)',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Filters'
    ],
    keywords='machine learning cnn svm bayesian',
    url='https://github.com/cahya-wirawan/opentc-util',
    author='Cahya Wirawan',
    author_email='Cahya.Wirawan@gmail.com',
    license='MIT',
    packages=find_packages('.'),
    package_dir={'': '.'},
    install_requires=[
        'PyYAML'
    ],
    scripts=[],
    data_files=[],
    include_package_data=True,
    zip_safe=False)
