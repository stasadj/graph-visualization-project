from setuptools import setup, find_packages
setup(
    name="complex-visualization",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['complex_visualization'],
    entry_points={
        'load.data':
            ['complex_visualization=complex_visualization.visualization:VisualizeService'],
    },
    zip_safe=True
)