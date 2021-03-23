from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['astunparse==1.6.3']

setup(
    name="astrologic",
    version="0.0.4",
    author="Evgeniy Blinov",
    author_email="zheni-b@yandex.ru",
    description="Автоматическая оптимизация кода на уровне АСТ",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pomponchik/astrologic",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
