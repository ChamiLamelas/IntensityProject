import numpy as np
from PIL import Image
from argparse import ArgumentParser
import pandas as pd
import os


def collect_args():
    """
    Sets up and collects necessary arguments using ArgumentParser. 

    Returns
    -------
        args : argparse.Namespace
            Namespace containing the arguments and their values specified by the user.
    """

    parser = ArgumentParser('Intensity Program')
    parser.add_argument(
        'dir', help='path to the directory where files matching \'root\' will be passed into program')
    parser.add_argument(
        'root', help='root name of files whose sums will be averaged over')
    parser.add_argument('row_start', type=int,
                        help='starting row, must be in [1,row_end]')
    parser.add_argument(
        'row_end', type=int, help='ending row, must be in [row_start,number of rows in image]')
    parser.add_argument('col_start', type=int,
                        help='starting column, must be in [1,col_end]')
    parser.add_argument(
        'col_end', type=int, help='ending column, must be in [row_start,number of columns in image]')
    parser.add_argument(
        'sum', help='whether you are summing over rows \'r\' or columns \'c\'')
    parser.add_argument(
        'out', help='path for the output file. for outputfile format, see docs for save_avgs()')
    args = parser.parse_args()
    return args


def prelim_check_args(args):
    """
    Preliminary argument check. This checks if:
    1. `args.row_start` is in `[1, row_end]`
    2. `args.col_start` is in `[1, col_end]`
    3. `args.sum` is in `{'r', 'c'}`

    Parameters
    ----------
    args : argparse.Namespace
        Namespace of arguments returned by `collect_args()`

    Raises
    ------
    ValueError
        If any of conditions 1-3 are not met. An appropriate error message is included.
    """

    if args.row_start < 1 or args.row_start > args.row_end:
        raise ValueError('row_start=%d is not in [1, row_end=%d]' % (
            args.row_start, args.row_end))
    if args.col_start < 1 or args.col_start > args.col_end:
        raise ValueError('col_start=%d is not in [1, col_end=%d]' % (
            args.col_start, args.col_end))
    if args.sum not in {'r', 'c'}:
        raise ValueError(
            '%s is not a valid input, must be \'r\' for rows or \'c\' for columns' % (args.sum))


def second_check_args(fname, args):
    """
    Secondary check of arguments. Opens a particular image file and checks if:
    1. `args.row_end` <= number of rows in the image
    2. `args.col_end` <= number of columns in the image

    Parameters
    ----------
    fname : str
        Name of the image file used to check conditions 1-2. It should be contained in `args.dir`.
    args : argparse.Namespace
        Namespace of arguments returned by `collect_args()`

    Raises
    ------
    ValueError
        If any of conditions 1-2 are not met. An appropriate error message is included.
    """

    fp = os.path.join(args.dir, fname)
    img = np.asarray(Image.open(fp))
    if args.row_end > img.shape[0]:
        raise ValueError('row_end=%d is not in [row_start,number of rows in image=%d]' % (
            args.row_end, img.shape[0]))
    if args.col_end > img.shape[1]:
        raise ValueError('col_end=%d is not in [col_start,number of columns in image=%d]' % (
            args.col_end, img.shape[1]))


def rmv_extra_channels(img):
    """
    If a greyscale image is stored as some color image, it will have 3 (RGB) color channels. Since we assume it is really greyscale, all the channels will have equal value so we create a new image of same width and height, but with just 1 color channel.

    Parameters
    ----------
    img : np.ndarray
        A numpy array that represents a colored image of dimensions (nr,nc,3)

    Returns
    -------
    gs_img : np.ndarray
        An array of dimensions (nr,nc) where `gs_img[i,j]` is `img[i,j,0]`
    """

    gs_img = np.zeros(img.shape[:2])
    for i in range(gs_img.shape[0]):
        for j in range(gs_img.shape[1]):
            gs_img[i, j] = img[i, j, 0]
    return gs_img


def compute_img_intensities(fname, args, shape):
    """
    Computes the intensities for a particular greyscale image. If it is stored as a color image, then extra channels are removed using `rmv_extra_channels()`.

    Parameters
    ----------
    fname : str
        Name of the image file
    args : argparse.Namespace
        Namespace of arguments returned by `collect_args()`
    shape : tuple
        Shape that the image should have. Ignored if `None`.

    Returns
    -------
    intensities : np.ndarray
        Numpy array with intensities summed over rows or columns based on user argument. It will be sized appropriately according to value of `args.sum`.
    shape : tuple
        Shape of image read in from `fname` in `args.dir`.

    Raises
    ------
    ValueError
        If the image stored at `fname` in `args.dir` does not have shape `shape` (for non `None` `shape`).
    """

    fp = os.path.join(args.dir, fname)
    img = np.asarray(Image.open(fp))
    curr_shape = img.shape
    if curr_shape != shape:
        raise ValueError('Image %s in %s is required to have %d rows, %d columns' % (
            fname, args.dir, shape[0], shape[1]))
    if len(img.shape) > 2:
        img = rmv_extra_channels(img)
    img = img[args.row_start-1:args.row_end, args.col_start-1:args.col_end]
    intensities = np.sum(img, axis=0 if args.sum == 'r' else 1)
    return intensities, curr_shape


def compute_avg_intensities(args):
    """
    For a set of files in directory `args.dir` that start with root `args.root`, find the average intensities across the region of interest specified by `args.row_start`, `args.row_end`, `args.col_start`, and `args.col_end`.

    Parameters
    ----------
    args : argparse.Namespace
        Namespace of arguments returned by `collect_args()`

    Returns
    -------
    avgs : np.ndarray
        Average itensities for each column if `args.sum == 'r'` or for each row if `args.sum == 'c'` in the ROIs for the file set described above.

    Raises
    ------
    ValueError
        See `compute_img_intensities()`
    """

    dir_intensities = []
    done_check = False
    shape = None
    for f in os.scandir(args.dir):
        if not f.name.startswith(args.root):
            continue
        if not done_check:
            second_check_args(f.name, args)
            done_check = True
        intensities, shape = compute_img_intensities(f.name, args, shape)
        dir_intensities.append(intensities)
    avgs = np.mean(np.array(dir_intensities), axis=0)
    return avgs


def save_avgs(avgs, args):
    """
    Saves the averages returned by `compute_avg_intensities()` to a CSV file with 2 columns.
    * If `args.sum == 'r'`, the 1st column has the columns of the ROI in `args` and the avg. intensity for each column
    * If `args.sum == 'c'`, the 1st column has the rows of the ROI in `args` and the avg. intensity for each row

    Parameters
    ----------
    avgs : np.ndarray
        Averages returned by `compute_avg_intensities()`
    args : argparse.Namespace
        Namespace of arguments returned by `collect_args()`
    """

    avgs = np.reshape(avgs, (avgs.shape[0], -1))
    if args.sum == 'r':
        idx = pd.Index(data=range(
            args.col_start, args.col_end+1), name='column')
    else:
        idx = pd.Index(data=range(args.row_start, args.row_end+1), name='row')
    df = pd.DataFrame(avgs, index=idx, columns=['average_intensity'])
    df.to_csv(args.out)


def main():
    """
    Main function: collects arguments, conducts preliminary check, computes average intensities and saves them.
    """

    args = collect_args()
    prelim_check_args(args)
    avgs = compute_avg_intensities(args)
    save_avgs(avgs, args)

if __name__ == '__main__':
    main()
