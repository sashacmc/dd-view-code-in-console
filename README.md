# dd-view-code-in-console
-----
Allow open code links from DataDog sites in console editors in the Linux or MacOS terminal emulator

## Linux
### Requriment
* Python 3.8 and above
* Pip
* Hatch (pip install hatch)

### Build
```console
hatch build
```

### Installation

```console
pip install dist/dd_view_code_in_console-*.whl
```

### Usage
Scan for git repositorines
```console
python3 -m dd_view_code_in_console -s PATH_TO_SOURCE_CODE
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
### Requriment
* Python 3.8 and above
* Pip
* iterm2 (pip install iterm2)

### Build
```console
python setup.py py2app -p iterm2
```

### Installation

Copy generated app from dist folder to applications.

You also need to enable the Python API for iTerm2:

(Prefs > General > Magic > Enable Python API)

### Usage
Scan for git repositorines
```console
/Applications/dd-view-code-in-console.app/Contents/MacOS/dd-view-code-in-console -s PATH_TO_SOURCE_CODE 
```
