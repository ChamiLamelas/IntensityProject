import numpy as np
from PIL import Image
from argparse import ArgumentParser
import pandas as pd
import os


def collect_args():
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
    parser.add_argument('out', help='path for the output file')
    args = parser.parse_args()
    return args


def prelim_check_args(args):
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
    fp = os.path.join(args.dir, fname)
    img = np.asarray(Image.open(fp))
    if args.row_end > img.shape[0]:
        raise ValueError('row_end=%d is not in [row_start,number of rows in image=%d]' % (
            args.row_end, img.shape[0]))
    if args.col_end > img.shape[1]:
        raise ValueError('col_end=%d is not in [col_start,number of columns in image=%d]' % (
            args.col_end, img.shape[1]))


def rmv_extra_channels(img):
    gs_img = np.zeros(img.shape[:2])
    for i in range(gs_img.shape[0]):
        for j in range(gs_img.shape[1]):
            gs_img[i, j] = img[i, j, 0]
    return gs_img


def compute_img_intensities(fname, args):
    fp = os.path.join(args.dir, fname)
    img = np.asarray(Image.open(fp))
    if len(img.shape) > 2:
        img = rmv_extra_channels(img)
    img = img[args.row_start-1:args.row_end, args.col_start-1:args.col_end]
    intensities = np.sum(img, axis=0 if args.sum == 'r' else 1)
    return intensities


def compute_avg_intensities(args):
    dir_intensities = []
    done_check = False
    for f in os.scandir(args.dir):
        if not f.name.startswith(args.root):
            continue
        if not done_check:
            second_check_args(f.name, args)
            done_check = True
        intensities = compute_img_intensities(f.name, args)
        dir_intensities.append(intensities)
    avgs = np.mean(np.array(dir_intensities), axis=0)
    return avgs


def save_avgs(avgs, args):
    avgs = np.reshape(avgs, (avgs.shape[0], -1))
    if args.sum == 'r':
        idx = pd.Index(data=range(
            args.col_start, args.col_end+1), name='column')
    else:
        idx = pd.Index(data=range(args.row_start, args.row_end+1), name='row')
    df = pd.DataFrame(avgs, index=idx, columns=['average_intensity'])
    df.to_csv(args.out)


def main():
    args = collect_args()
    prelim_check_args(args)
    avgs = compute_avg_intensities(args)
    save_avgs(avgs, args)


main()
