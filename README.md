# dd-view-code-in-console

-----

## Requriment
* Python 3.8 and above
* Pip
* Hatch (pip install hatch)

## Build
```console
hatch build
```

## Installation

```console
pip install dist/dd-view-code-in-console*
```

## Add schema handler
### Linux
Copy desktop entry file
```console
cp resources/ddcode-opener.desktop ~/.local/share/applications/
```
Configure scheme handler
```console
xdg-mime default ddcode-opener.desktop x-scheme-handler/ddcode
```


