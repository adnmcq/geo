import pandas as pd
import numpy as np
import time, os

BASE_DIR='C:\\Users\\aidenm\\Desktop\\geo'

rt_df = pd.read_csv(os.path.join(BASE_DIR, 'test_route.txt'))
'''
lon, lat
-118.410339, 34.019653
-118.410805, 34.020241
-118.411301, 34.020863
-118.411766, 34.021458
...
'''

fm_df = pd.read_csv(os.path.join(BASE_DIR, 'test_fm.txt'))
'''
lat, lon
41.033959, -77.515672
41.785524, -80.853175
41.128748, -80.769934
41.465085, -82.060677
...
'''



def is_on_route_inline(x, route_coordinates):
    '''

    :param route_coordinates:
    :param fencing_module_coordinate:
    :return: True if on route else False
    '''



    a = np.array((float(x[0]), float(x[1])))
    # bs = [np.array((c[1], c[0])) for c in rcs]


    def distance_inline(b, fcm_point):
        return np.linalg.norm(b-fcm_point)

    # bss = pd.Series(bs)
    distances = route_coordinates.apply(distance_inline, args=(a,), axis=1)   #np.linalg.norm(a-b))

    # distances = [np.linalg.norm(a-b) for b in bs]

    if min(distances)<0.1:
        print(x)
        return True

    return False

fm_df.apply(is_on_route_inline,  args=(rt_df,), axis=1)#rt_df)

