import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='lightchain',
    version='0.0.6',
    author='Andrew Parry',
    author_email='a.parry.1@research.gla.ac.uk',
    description="Stupidly Simple Chain Structures",
    requires=requirements,
    url='https://github.com/Parry-Parry/LightChain',
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires='>=3.6',
)
