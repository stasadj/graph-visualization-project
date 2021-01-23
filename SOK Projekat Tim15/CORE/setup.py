from setuptools import setup, find_packages

setup(
    name="core-django-app",
    version="0.1",
    packages=find_packages(),
    install_requires=['Django>=2.1'],
    package_data={'core_django_app': ['static/*.css', 'static/*.js', 'static/*.html', 'templates/*.html']},
    zip_safe=False
)