from setuptools import setup, find_packages
setup(
    name="simple-visualization",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['simple_visualization'],
    entry_points={
        'visualize.data':
            ['simple_visualization=simple_visualization.visualization:SimpleVisualization'],
    },
    zip_safe=True
)
