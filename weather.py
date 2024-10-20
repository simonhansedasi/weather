import numpy as np
import matplotlib.pyplot as plt


def create_data_windows(data, hours = 24):
    hours = 24 

    windows = {}

    num_windows = len(data['dt']) // hours  

    for i in range(num_windows):
        start_index = i * hours
        end_index = start_index + hours
        window = {key: data[key][start_index:end_index] for key in data.keys()}
        windows[start_index] = window

    print(f"Number of windows created: {len(windows)}")
    return windows








def detect_rain_events(data, target_column, build_hours = 12, trail_hours = 12):
    # rain = data['rain_1h'].flatten()
    no_of_rain_events = 0
    i = 0
    rain_windows = []
    rain_events = 0
    while i < len(target_column):
    
        if not np.isnan(target_column[i]):  # rain event detected                    
            rain_start = i                           
            rain_window_start = i - build_hours     
            rain_end = rain_start




            while rain_end < len(target_column) and not np.isnan(target_column[rain_end]):  # tick until the end of the rain event
                rain_end += 1



            if rain_end + trail_hours < len(target_column) and all(np.isnan(target_column[rain_end:rain_end+trail_hours])):  # rain event ends when field is nan
                rain_window_end = min(len(target_column), rain_end + trail_hours)   # index of rain end window

                rain_window = {key: data[key][rain_window_start:rain_window_end] for key in data}
                rain_windows.append(rain_window)
                no_of_rain_events += 1


            i = rain_end   # reset i s/t we don't encounter this event again

        else:
            i += 1
        
    return rain_windows




def split_data(X,Y,frac = 0.2):
    n_samples = np.shape(X)[0]
    
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    
    # X_shuffled = X[indices]
    # Y_shuffled = Y[indices]
    
    split_index = int(n_samples * (1 - frac))
    
    X_tr = X[:split_index]
    X_te = X[split_index:]
    
    Y_tr = Y[:split_index]
    Y_te = Y[split_index:]
    
    return np.array(X_tr), np.array(X_te), np.array(Y_tr), np.array(Y_te)



def pad_arrays(array, max_length):
    full_padded_array = []
    for arr in array:
        # print(arr)
        if array.ndim ==1 :
            num_nans_to_add = max_length - len(arr)
            array_pad = np.full((num_nans_to_add, 1), 0.0).flatten()

            padded_array = np.concatenate((arr, array_pad), axis = 0)

            padded_array = np.array(padded_array)

            full_padded_array.append(padded_array)

        if array.ndim == 2 :
            num_nans_to_add = max_length - len(arr[0])

            array_pad = np.full((num_nans_to_add, 1), 0.0).flatten()

            padded_arrays = []
            for i in range(7):
                padded_array = np.concatenate((arr[i], array_pad), axis = 0)
                # print(arr[i])
                padded_arrays.append(padded_array)

            padded_arrays = np.array(padded_arrays)
            full_padded_array.append(padded_arrays)


        
    return np.array(full_padded_array)


def min_max_normalize(matrix):
    min_val = np.nanmin(matrix)
    max_val = np.nanmax(matrix)
    
    normalized_matrix = (matrix - min_val) / (max_val - min_val)
    
    return normalized_matrix


def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    
    
def inverse_min_max_normalize(normalized_matrix, original_matrix):
    min_val = np.nanmin(original_matrix)
    max_val = np.nanmax(original_matrix)
    return normalized_matrix * (max_val - min_val) + min_val