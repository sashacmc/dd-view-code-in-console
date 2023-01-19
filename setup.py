from setuptools import setup

setup(
    app=["dd_view_code_in_console/__main__.py"],
    setup_requires=["py2app"],
    options=dict(
        py2app=dict(
            argv_emulation=True,
            plist=dict(
                CFBundleURLTypes=[
                    dict(CFBundleURLName="URLHandler", CFBundleURLSchemes=["ddcode"])
                ]
            ),
        )
    ),
)
