import hdf5storage
file_path = '../origin_2class/label_1_data.mat'
mat_contents = hdf5storage.loadmat(file_path)
print(mat_contents.keys())