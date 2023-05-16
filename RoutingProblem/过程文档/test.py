
data = {}
weights = [48, 30, 42, 36, 36, 48, 42, 42, 36, 24, 30, 30, 42, 36, 36]
values = [10, 30, 25, 50, 35, 30, 15, 40, 30, 35, 45, 10, 20, 30, 25]
data['weights'] = weights
data['values'] = values
data['items'] = list(range(len(weights)))
data['num_items'] = len(weights)
num_bins = 5
data['bins'] = list(range(num_bins))
data['bin_capacities'] = [100, 100, 100, 100, 100]

print([data['weights'][i] for i in [2,4,6]])