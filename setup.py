import  setuptools


setuptools.setup(
    name="animation_framework",
    description="Framework for Animation over OPC and OSC",
    version="0.1",
    packages=setuptools.find_packages(),
    #packages=[
    #    'animation_framework',
    #    'animation_framework.midi'
    #],
    install_requires=[
        "pyOSC==0.3.5b5294",
        "numpy==1.13.1"
    ],
    extra_requires={
        'midi': ['mido']
    },
    entry_points={
        'animation_framework.plugins.config': [
            'midi=animation_framework.plugins.midi:configure_parser'
        ],
        'animation_framework.plugins.listeners': [
            'keyboard=animation_framework._keyboard:launch_keyboard_thread',
            'midi=animation_framework.plugins.midi:register_listeners'
        ],
        'animation_framework.plugins.layout': [
            'midi=animation_framework.plugins.midi:annotate_layout'
        ]
    }

)
