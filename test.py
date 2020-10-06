import pandas as pd
import numpy as np
import time, os, platform

if platform.system() == 'Windows':
    lt = '\r'
else:
    lt = '\n'


BASE_DIR='C:\\Users\\aidenm\\Desktop\\geo'

rt_df = pd.read_csv(os.path.join(BASE_DIR, 'test_route.txt'))#, lineterminator=lt)

cols = rt_df.columns.tolist()
rev = cols[-1:] + cols[:-1]
rt_df = rt_df[rev]
'''
lon, lat
-118.410339, 34.019653
-118.410805, 34.020241
-118.411301, 34.020863
-118.411766, 34.021458
...
'''

fm_df = pd.read_csv(os.path.join(BASE_DIR, 'test_fm.txt'))#,  lineterminator=lt)
'''
lat, lon
41.033959, -77.515672
41.785524, -80.853175
41.128748, -80.769934
41.465085, -82.060677
...
'''


from scipy.spatial import distance_matrix

route_points = rt_df.values  # shape (100k, 2)
truck_points = fm_df.values  # shape (800, 2)

print(type(route_points), type(truck_points))
print(np.shape(route_points), np.shape(truck_points))

all_distances = distance_matrix(route_points, truck_points)

# print(all_distances)# shape (100k, 800)

zz=[]
for col, fmc in zip(all_distances.T, truck_points):
    if min(col) <0.1:
        # print(min(col), fmc)
        zz.append(fmc)

print(zz)


# fencing_modules_with_distance_to_routes = np.array([[a, b] for a, b in zip(all_distances.T, truck_points)])
# # mask = z[:, 0] == 6
# # z[mask, :]
#
# mask = fencing_modules_with_distance_to_routes[:, 0]<0.1
# fencing_modules_with_distance_to_routes[mask, :]


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

# fm_df.apply(is_on_route_inline,  args=(rt_df,), axis=1)#rt_df)

