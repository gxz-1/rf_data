
import hdf5storage
file_path_prefix = "/home/lbt/dataset/origin_USRP0326/merged/7_merged_data.mat"

originData = hdf5storage.loadmat(file_path_prefix)['data']
# print(originData.keys())
print(originData.shape)

print(originData[:5]) 

#  (125052, 4096)
# (82695, 4096)
# (106899, 4096)
#  (195646, 4096)