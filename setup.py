import  setuptools


setuptools.setup(
    name="simple_af",
    description="Framework for Animation over OPC and OSC",
    version="0.1",
    #packages=setuptools.find_packages(),
    packages=[
        'simple_af',
        'simple_af.plugins.midi',
        'simple_af.plugins.stock_effects'
    ],
    install_requires=[
        "pyOSC==0.3.5b5294",
        "numpy==1.13.1"
    ],
    extra_requires={
        'midi': ['mido']
    },
    entry_points={
        'simple_af.plugins.config': [
            'midi=simple_af.plugins.midi:configure_parser'
        ],
        'simple_af.plugins.listeners': [
            'keyboard=simple_af._keyboard:launch_keyboard_thread',
            'midi=simple_af.plugins.midi:register_listeners'
        ],
        'simple_af.plugins.layout': [
            'midi=simple_af.plugins.midi:annotate_layout'
        ]
    }

)
