from setuptools import setup, find_packages

setup(
    name='FastPriceViz',
    version='0.1.0',
    description='A library for visualization of high-frequency time series data',
    author='David Levy',
    author_email='dlevy457@gmail.com',
    url='https://github.com/dlevy233/FastPriceViz',
    license='MIT',
    packages=find_packages(exclude=['tests', 'docs', 'examples']),  # Exclude non-package directories
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'dask[complete]>=2021.0.0',
        'bokeh>=2.0.0',
        'pyarrow>=1.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Adjust as appropriate
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',  # Specify supported Python versions
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    include_package_data=True,  # Include files specified in MANIFEST.in
    keywords='time series visualization dask bokeh',
    project_urls={
        'Source': 'https://github.com/dlevy233/FastPriceViz',
    },
)
