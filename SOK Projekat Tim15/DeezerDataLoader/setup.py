from setuptools import setup, find_packages
setup(
    name="deezer-data-loader",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['deezer_load'],
    install_requires=['requests >= 2.25.1'],
    entry_points={
        'load.data':
            ['load_deezer_data=deezer_load.load_deezer_data:LoadDeezerData'],
    },
    zip_safe=True
)
