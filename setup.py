from os import path

from setuptools import find_packages, setup

loc = path.abspath(path.dirname(__file__))

with open(loc + "/requirements.txt") as f:
    requirements = f.read().splitlines()

required = []
dependency_links = []

# Do not add to required lines pointing to Git repositories
EGG_MARK = "#egg="
for line in requirements:
    if (
        line.startswith("-e git:")
        or line.startswith("-e git+")
        or line.startswith("git:")
        or line.startswith("git+")
    ):
        line = line.lstrip("-e ")  # in case that is using "-e"
        if EGG_MARK in line:
            package_name = line[line.find(EGG_MARK) + len(EGG_MARK) :]
            repository = line[: line.find(EGG_MARK)]
            required.append("%s @ %s" % (package_name, repository))
            dependency_links.append(line)
        else:
            print("Dependency to a git repository should have the format:")
            print("git+ssh://git@github.com/xxxxx/xxxxxx#egg=package_name")
    else:
        required.append(line)

setup(
    name="github_poster",
    author="yihong0618",
    author_email="zouzou0208@gmail.com",
    url="https://github.com/yihong0618/GitHubPoster",
    license="MIT",
    version="1.4.0",
    description="Make everything a GitHub svg poster and Skyline!",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    dependency_links=dependency_links,
    entry_points={
        "console_scripts": ["github_poster = github_poster.cli:main"],
    },
)
