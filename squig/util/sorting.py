from helper.Error import RunTimeError

def merge(arr, start, mid, end):

    start2 = mid + 1

    # If the direct merge is already sorted
    if arr[mid].value <= arr[start2].value:
        return

    # Two pointers to maintain start of both arrays to merge
    while start <= mid and start2 <= end:
        # If element 1 is in right place
        if arr[start].value <= arr[start2].value:
            start += 1
        else:
            value = arr[start2]
            index = start2

            # Shift all the elements between element 1 and element 2 right by 1
            while index != start:
                arr[index] = arr[index - 1]
                index -= 1

            arr[start] = value

            # Update all the pointers
            start += 1
            mid += 1
            start2 += 1

def merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2

        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)

        try :
            merge(arr, l, m, r)
        except Exception as e:
            return RunTimeError("check sorting.py" , e)
        return None