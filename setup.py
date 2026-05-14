from setuptools import setup, find_packages

setup(
    name="cmmc2",
    version="1.0.0",
    description="CMMC 2.0 compliance assessment tool — NIST SP 800-171 Rev 2, SPRS scoring, POAM generation",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "cmmc2=cmmc2.cli:main",
        ],
    },
)
