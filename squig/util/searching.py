def linear_search(array, value):

    for index in range(len(array)):
        
        if array[index].value == value:
            return index

    return -1

def interpolationSearch(arr, n, x): 
   
    low = 0
    high = (n - 1) 
   
    while low <= high and x >= arr[low].value and x <= arr[high].value: 
        if low == high: 
            if arr[low] == x: 
                return low; 
            return -1; 
   
        pos = int(low + (((float(high - low)/( arr[high].value - arr[low].value)) * (x - arr[low].value)))) 
   
        if arr[pos].value == x: 
            return pos 
   
        if arr[pos].value < x: 
            low = pos + 1; 
   
        else: 
            high = pos - 1; 
       
    return -1