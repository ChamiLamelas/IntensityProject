:: Sample batch file, replace with appropriate parameters
:: Here, ROI is rows [1,3] and columns [2,4]
python intensity.py "<dir1>" "<root>" 1 3 2 4 "r" "<path to outputs>/output1_r.csv"
python intensity.py "<dir1>" "<root>" 1 3 2 4 "c" "<path to outputs>/output1_c.csv"
python intensity.py "<dir2>" "<root>" 1 3 2 4 "r" "<path to outputs>/output2_r.csv"
python intensity.py "<dir2>" "<root>" 1 3 2 4 "c" "<path to outputs>/output2_c.csv"