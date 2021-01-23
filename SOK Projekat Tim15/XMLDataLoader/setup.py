from setuptools import setup, find_packages
setup(
    name="xml-data-loader",
    version="0.1",
    packages=find_packages(),
    namespace_packages=['xml_load'],
    entry_points={
        'load.data':
            ['load_xml_data=xml_load.load_xml_data:LoadXMLData'],
    },
    zip_safe=True
)