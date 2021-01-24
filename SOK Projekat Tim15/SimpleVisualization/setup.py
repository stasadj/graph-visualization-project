from setuptools import setup, find_packages
setup(
    name="simple-visualization",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['simple_visualization'],
    package_data={'simple_visualization': ['*.js']},
    entry_points={
        'visualize.data':
            ['simple_visualization=simple_visualization.simple_visualization:SimpleVisualization'],
    },
    zip_safe=True
)
