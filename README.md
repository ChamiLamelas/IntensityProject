# Intensity Project

This is a Python program used for averaging intensities summed over rows or columns in a specified region of interest for a collection of files of equal dimensions.

## Dependencies

- Download Python 3.9.1+ from [here](https://www.python.org/downloads/).
- Install [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/), and the Python Image Library via [Pillow fork](https://pypi.org/project/Pillow/). This can be done with `pip` (the Python package manager installed with Python) by typing these commands in a terminal window:

  ```
  pip install numpy
  pip install pandas
  pip install pillow
  ```

  You can check that everything has been installed properly, with the following command:

  ```
  pip list
  ```

  Make sure that entries for `numpy`, `pandas`, and `Pillow` appear there.

  Or, if you're on Windows, just download and run `dependencies.bat` by double clicking it.

- Make sure that the images you pass in are supported by PIL. Open a terminal and run the following:

  ```
  python -m PIL
  ```

  Make sure that the file types you are interested in have `open` listed right of `Features:` in the command's displayed output. For example, BMP, JPEG, PNG, and TIFF file formats all have this property.

## How to Use

First, download `intensity.py`. To receive updates more smoothly, you can install `git` and clone the repository instead. In this section, I will discuss a few examples of how to run this program on Windows.

For more information on the code, you can download and view `intensity.html` for documentation in a browser.

### Scenario 1: `intensity.py`, data, and output directory in same folder

Suppose you have stored `intensity.py`, your data in a folder called `data`, and created a folder `output` for your program outputs in the directory:

```
C:\Users\Chami\programming\python\intensity_project
```

Open Command Prompt by pressing the Windows key and typing `cmd`. Navigate to this directory using `cd`. The directory you are currently in the command line (or equivalently where you have placed a batch file with commands) is known as the Current Working Directory (CWD). Typing `dir` in this directory would include:

```
data
intensity.py
output
```

If you run this command:

```
python intensity.py -h
```

`-h` will tell us how to use the intensity program. The output is shown below. It tells us (i) which arguments must be specified and (ii) the order they must be placed in.

```
usage: python intensity.py [-h] dir root row_start row_end col_start col_end sum out

positional arguments:
  dir         path to the directory where files matching root will be passed into program
  root        root name of files whose sums will be averaged over (case-sensitive)
  row_start   starting row, must be an integer in [1,row_end]
  row_end     ending row, must be an integer in [row_start,number of rows in image]
  col_start   starting column, must be an integer in [1,col_end]
  col_end     ending column, must be an integer in [row_start,number of columns in image]
  sum         whether you are summing over rows "r" or columns "c"
  out         path for the output file. for outputfile format, see docs for save_avgs()

optional arguments:
  -h, --help  show this help message and exit
```

Suppose that we want to average row-summed intensities for all files starting with `data_a` over the Region Of Interest (ROI) of rows 1 to 3 and columns 2 to 4. Furthermore, suppose we want to save the average intensities per column to `output_a.csv`. Our argument settings would be:

```
dir = "data"
root = "data_a"
row_start = 1
row_end = 3
col_start = 2
col_end = 4
sum = "r"
out = "output/output_a.csv"
```

With the exception of the ROI arguments which are integers, all the other arguments are surrounded in `""` as they are strings. Following the `-h` information, the command would be:

```
python intensity.py "data" "data_a" 1 3 2 4 "r" "output/output_a.csv"
```

This command is included in the batch file `scenario1.bat` which would be placed in the CWD:

```
C:\Users\Chami\programming\python\intensity_project
```

To run a batch file, double click it. To edit it, right click and choose Edit. In the three scenario batch files, they start with `@echo off` to make the display cleaner and `pause` so the user can see the program output in a Command Prompt window. Otherwise, the window will immediately close on termination. `pause` is useful to check for any errors displayed in the program output.

> _Note:_ If you look at file paths in Windows you will see that they have backslashes `\` as opposed to forward slashes `/`. However, you can use either. It is easier when working with strings however to use `/` because `\` is the special [escape character](https://python-reference.readthedocs.io/en/latest/docs/str/escapes.html) in Python. That is, it is used in conjunction with the following letter to represent special characters (`\n` means a newline, `\t` a tab, etc.). To represent a `\` in Python you need to escape it. Thus, to store the path `C:\Users\Chami` in a Python string, you would need to write it as either `"C:/Users/Chami"` or `"C:\\Users\\Chami"`.

### Scenario 2: `intensity.py`, output directory in CWD and data in different folder

Suppose you have stored `intensity.py` and created a folder `output` for your program outputs in the directory:

```
C:\Users\Chami\programming\python\intensity_project
```

Open Command Prompt and navigate to this directory using `cd`.

Suppose your data is stored in a folder `data` located at:

```
C:\Users\Chami\experiments
```

Like in Scenario 1, suppose that we want to average row-summed intensities for all files starting with `data_a` over the ROI of rows 1 to 3 and columns 2 to 4. Furthermore, suppose we want to save the average intensities per column to `output_a.csv`. The `root`, the ROI arguments, and `sum` all remain the same from Scenario 1. The CWD is:

```
C:\Users\Chami\programming\python\intensity_project
```

Therefore, `out` remains the same `output/output_a.csv`. The one argument we have to change is `dir`. One strategy is to specify the full or _absolute_ path to the data:

```
dir = "C:/Users/Chami/experiments"
```

`/` or `\\` could be used as discussed in the note following Scenario 1. We can also use a relative path making use of the special path `..` in a relative path. `..` means the parent directory. For instance, if we type `cd ..` into Command Prompt we go up one directory. `cd ../..` goes up two directories. `data` is in `experiments` which is in `Chami` which is the **3rd** directory up from the CWD. Hence, we could alternatively define:

```
dir = "../../../experiments/data"
```

Thus, we could run either:

```
python intensity.py "C:/Users/Chami/experiments/data" "data_a" 1 3 2 4 "r" "output/output_a.csv"
```

Or

```
python intensity.py "../../../experiments/data" "data_a" 1 3 2 4 "r" "output/output_a.csv"
```

The first command is included in the batch file `scenario2.bat` which would be placed in the CWD:

```
C:\Users\Chami\programming\python\intensity_project
```

### Scenario 3: `intensity.py`, output directory in different folder and data in CWD

Suppose your data is stored in a folder `data` located at:

```
C:\Users\Chami\experiments
```

Open Command Prompt and navigate to this directory using `cd`.

Like in Scenarios 1 and 2, suppose you have stored `intensity.py` and created a folder `output` for your program outputs in the directory:

```
C:\Users\Chami\programming\python\intensity_project
```

Like in Scenarios 1 and 2, suppose that we want to average row-summed intensities for all files starting with `data_a` over the ROI of rows 1 to 3 and columns 2 to 4. The `root`, the ROI arguments, and `sum` all remain the same from Scenarios 1 and 2. _Unlike_ Scenarios 1 and 2, the CWD is:

```
C:\Users\Chami\experiments
```

More importantly, the CWD is **not** the folder where the program is located. Like in Scenario 1, the data folder `data` is in the CWD, hence `dir = "data"`. The output folder `output`, like the data folder in Scenario 2 is not CWD hence we must specify its location using an absolute path:

```
out = "C:/Users/Chami/programming/python/intensity_project/output/output_a.csv"
```

Or with a relative path:

```
out = "../programming/python/intensity_project/output/output_a.csv"
```

Similarly, our command can no longer start with `python intensity.py` as `intensity.py` is not in the CWD. In fact, `intensity.py` is actually the first argument passed to the command `python`. The following arguments are also arguments of `python` but are automatically passed to the `intensity.py` program. Thus, we have to specify the path to `intensity.py` using either an absolute path or relative path similar to the two above.

Thus, a command we can use in this scenario is:

```
python C:/Users/Chami/programming/python/intensity_project/intensity.py "data" "data_a" 1 3 2 4 "r" "C:/Users/Chami/programming/python/intensity_project/output/output_a.csv"
```

We could have written a command using relative paths, but it is probably best to keep 1 copy of `intensity.py` in a central folder and use absolute paths when executing commands from different experiment folders. Otherwise, you may have to rederive relative paths based on the structuring of your data folders. If you want to collect your outputs in the one spot, you should use absolute paths in that case for the same reason.

This command is included in the batch file `scenario3.bat` which would be placed in the CWD:

```
C:\Users\Chami\experiments
```

## Output

The program outputs a CSV file with 2 columns.

- If `sum == "r"`, the 1st column (titled `column`) has the columns of the ROI and the 2nd column (titled `average_intensity`) has the average intensity for each column.
- If `sum == "c"`, the 1st column (titled `row`) has the rows of the ROI and the 2nd column (titled `average_intensity`) has the average intensity for each row.

## Built With

- [Python 3.9.1](https://www.python.org/downloads/) - Python version. View the list of versions on the website.
- [Visual Studio Code](https://code.visualstudio.com/) - Local IDE.
- [pdoc3](https://pdoc3.github.io/pdoc/) - documentation package, one of [many](https://wiki.python.org/moin/DocumentationTools).
- [NumPy](https://numpy.org/) - linear algebra / matrix operations.
- [pandas](https://pandas.pydata.org/) - CSV creation.
- [Pillow](https://pypi.org/project/Pillow/) - image loading.

## Authors

- **Chami Lamelas** - _Developer_ -
  [my personal GitHub](https://github.com/ChamiLamelas)

## Acknowledgments

- [gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore) - gitignore file for Python files
