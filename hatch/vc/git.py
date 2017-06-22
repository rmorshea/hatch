import os
import subprocess

from hatch.ignore import GitIgnore
from hatch.structures import File


class GitAttributes(File):
    def __init__(self):
        super(GitAttributes, self).__init__(
            '.gitattributes',
            (
                '# Auto detect text files and perform LF normalization\n'
                '* text=auto\n'
            )
        )


def setup_git(d, package_name):
    if not os.path.exists(os.path.join(d, '.git')):  # no cov
        try:
            subprocess.call('git init --quiet')
        except:
            print('Could not find "git" executable')
        GitAttributes().write(d)
        GitIgnore(package_name).write(d)
