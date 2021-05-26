# Intensity Project

## Dependencies
* Download Python 3.9.1+ from [here](https://www.python.org/downloads/).
* Install Python Image Library via [Pillow fork](https://pypi.org/project/Pillow/). This can be done with `pip` (the Python package manager installed with Python) by typing this command in a terminal window:
    ```
    pip install pillow
    ```

## How to Use
Once you have downloaded `intensity.py`. Navigate to its directory in a terminal. Then, type:
```
python intensity.py -h
```
So that you can see help information on what parameters to use and how to use them.

To ensure that the images you will be passing in are readable by `PIL`, open a terminal and run the following command:
```
python -m PIL
```
Make sure that the file types you are interested in have `open` listed right of `Features:` in the command's displayed output. For example, BMP, JPEG, PNG, and TIFF file formats all have this property.

You can also automate multiple commands (and to make editing parameters easier) by running a batch file if you're on Windows. `experiments.bat` is an example.

For more information on the code, you can download and view `intensity.html` for documentation in a browser.

## Built With

* [Python 3.9.1](https://www.python.org/downloads/) - Python version. View the list of versions on the website.
* [Visual Studio Code](https://code.visualstudio.com/) - Local IDE.
* [pdoc3](https://pdoc3.github.io/pdoc/) - documentation package, one of [many](https://wiki.python.org/moin/DocumentationTools).

## Authors

* **Chami Lamelas** - *Developer* - 
[my personal GitHub](https://github.com/ChamiLamelas)

## Acknowledgments

* [gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore) - gitignore file for Python files
