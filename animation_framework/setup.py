import  setuptools


setuptools.setup(
    name="animation_framework",
    version="0.1",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyOSC==0.3.5b5294"
    ],
    description="Framework for Animation over OPC and OSC"
)
