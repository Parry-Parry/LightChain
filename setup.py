import setuptools

setuptools.setup(
    name='lightchain',
    version='0.0.5',
    author='Andrew Parry',
    author_email='a.parry.1@research.gla.ac.uk',
    description="Stupidly Simple Chain Structures",
    url='https://github.com/Parry-Parry/LightChain',
    packages=setuptools.find_packages(exclude=['tests', 'lightchain_tmp']),
    python_requires='>=3.6',
)
