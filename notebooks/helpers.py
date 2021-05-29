import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime

def month_n2s(n):
    if n == 10:
        return 'Oct'
    elif n == 11:
        return 'Nov'
    elif n == 12:
        return 'Dec'
    elif n == 1:
        return 'Jan'
    elif n == 2:
        return 'Feb'
    elif n == 3:
        return 'March'
    elif n == 4:
        return 'April'
    elif n == 5:
        return 'May'
    elif n == 6:
        return 'June'
    elif n == 7:
        return 'July'
    elif n == 8:
        return 'August'
    else:
        return 'Sep'