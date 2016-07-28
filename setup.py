import pip
from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements("requirements/base.txt",
                                  session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]


setup(
    name='cielo24_utils',
    version='0.0.3',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=reqs,
    description='python utils for cielo apps',
    author='cielo24',
    author_email='devs@cielo24.com',
)
