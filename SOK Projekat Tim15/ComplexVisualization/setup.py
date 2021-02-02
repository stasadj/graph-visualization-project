from setuptools import setup, find_packages
setup(
    name="complex-visualization",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['complex_visualization'],
    package_data={'complex_visualization': ['*.js']},
    entry_points={
        'visualize.data':
            ['complex_visualization=complex_visualization.visualization:ComplexVisualization'],
    },
    zip_safe=True
)