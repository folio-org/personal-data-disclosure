from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="github-pdd-scan",
    description="Scan GitHub repositories for PERSONAL_DATA_DISCLOSURE documents",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Peter Murray",
    url="https://github.com/folio-org/personal-data-disclosure/scripts/github-pdd-scan",
    project_urls={
        "Issues": "https://issues.folio.org/projects/FOLIO/summary",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["github_pdd_scan"],
    entry_points="""
        [console_scripts]
        github-pdd-scan=github_pdd_scan.cli:cli
    """,
    install_requires=["click"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.6",
)
