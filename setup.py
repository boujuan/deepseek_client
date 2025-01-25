import setuptools

setuptools.setup(
    name="deepseek-r1-client",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyyaml",
        "cryptography",
        "replicate",
        "openai",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "deepseek=deepseek.main:main_entry",
        ],
    },
) 