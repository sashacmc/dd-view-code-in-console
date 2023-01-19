# dd-view-code-in-console
-----
Allow open code links from DataDog sites in console editors

## Requriment
* Python 3.8 and above
* Pip
* Hatch (pip install hatch)

## Linux
### Build
```console
hatch build
```

### Installation

```console
pip install dist/dd_view_code_in_console-*.whl
```

### Add schema handler
Copy desktop entry file
```console
cp resources/ddcode-opener.desktop ~/.local/share/applications/
```
Configure scheme handler
```console
xdg-mime default ddcode-opener.desktop x-scheme-handler/ddcode
```
## MacOS
### Build
```console
python setup.py py2app -p iterm2
```

### Installation

Copy generated app from dist folder to applications
