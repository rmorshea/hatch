from hatch.structures import File
from hatch.utils import normalize_package_name

BASE = """\
from setuptools import find_packages, setup

with open('{package_name_normalized}/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('= ')[1].strip('\\'"')
            break

requires = []

with open('requirements.txt', 'r') as f:
    for line in f.readlines():
        req = line.strip()
        if req:
            requires.append(req)

setup(
    name='{package_name}',
    version=version,
    description='',
    long_description=open('{readme_file}', 'r').read(),
    author='{name}',
    author_email='{email}',
    maintainer='{name}',
    maintainer_email='{email}',
    url='{package_url}',
    download_url='{package_url}',
    license='{license}',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',{license_classifiers}
        'Natural Language :: English',
        'Operating System :: OS Independent',{pyversions}
        'Programming Language :: Python :: Implementation :: CPython',{pypy}
    ],

    install_requires=requires,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),{entry_point}
)
"""


class SetupFile(File):
    def __init__(self, name, email, package_name, pyversions, licenses, readme,
                 package_url, cli):
        normalized_package_name = normalize_package_name(package_name)

        pypy = ''
        versions = ''
        for pyversion in pyversions:
            if not pyversion.startswith('pypy'):
                versions += "\n        'Programming Language :: Python :: {}',".format(
                    pyversion
                )
            else:
                pypy = "\n        'Programming Language :: Python :: Implementation :: PyPy',"

        license_classifiers = ''
        for li in licenses:
            license_classifiers += "\n        '{}',".format(li.pypi_classifier)

        if not cli:
            entry_point = ''
        else:
            entry_point = (
                '\n'
                '    entry_points={{\n'
                "        'console_scripts': [\n"
                "            '{pn} = {pnn}.cli:{pnn}',\n"
                '        ],\n'
                '    }},'.format(pn=package_name, pnn=normalized_package_name)
            )

        super(SetupFile, self).__init__(
            'setup.py',
            BASE.format(
                name=name,
                email=email,
                package_name=package_name,
                package_name_normalized=normalized_package_name,
                readme_file=readme.file_name,
                package_url=package_url,
                license='/'.join(li.short_name for li in licenses),
                license_classifiers=license_classifiers,
                pyversions=versions,
                pypy=pypy,
                entry_point=entry_point
            )
        )
