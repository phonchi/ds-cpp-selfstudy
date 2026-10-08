"""Verbatim function bodies from pythonds3/cppds/sorting.hpp and searching.hpp (shown in folded cards).
Keep in sync with the course headers; docs/verification/20261008-ch7/check_content.py compares them."""

HPP = {
    'printl': r'''void printl(vector<int>& aList) {
    for (int x : aList) cout << x << " ";
    cout << endl;
}''',
    'bubbleSort': r'''void bubbleSort(vector<int>& aList) {
    for (int i = aList.size() - 1; i > 0; i--) {
        printl(aList);
        for (int j = 0; j < i; j++) {
            if (aList[j] > aList[j + 1]) {
                int temp = aList[j];
                aList[j] = aList[j + 1];
                aList[j + 1] = temp;
            }
        }
    }
}''',
    'bubbleSortShort': r'''void bubbleSortShort(vector<int>& aList) {
    for (int i = aList.size() - 1; i > 0; i--) {
        bool exchanges = false;
        for (int j = 0; j < i; j++) {
            if (aList[j] > aList[j + 1]) {
                exchanges = true;
                swap(aList[j], aList[j + 1]);
            }
        }
        if (!exchanges) break;
    }
}''',
    'selectionSort': r'''void selectionSort(vector<int>& aList) {
    int n = static_cast<int>(aList.size());
    for (int fillSlot = n - 1; fillSlot > 0; fillSlot--) {
        printl(aList);
        int positionOfMax = 0;
        for (int location = 1; location <= fillSlot; location++) {
            if (aList[location] > aList[positionOfMax]) {
                positionOfMax = location;
            }
        }
        if (positionOfMax != fillSlot) {
            swap(aList[positionOfMax], aList[fillSlot]);
        }
    }
}''',
    'insertionSort': r'''void insertionSort(vector<int>& aList) {
    for (unsigned i = 1; i < aList.size(); i++) {
        printl(aList);
        int curVal = aList[i];
        int curPos = i;
        while (curPos > 0 && aList[curPos - 1] > curVal) {
            aList[curPos] = aList[curPos - 1];
            curPos = curPos - 1;
        }
        aList[curPos] = curVal;
    }
}''',
    'gapInsertionSort': r'''void gapInsertionSort(vector<int>& aList, int start, int gap) {
    for (unsigned i = start + gap; i < aList.size(); i += gap) {
        int curVal = aList[i];
        int curPos = i;
        while (curPos >= gap && aList[curPos - gap] > curVal) {
            aList[curPos] = aList[curPos - gap];
            curPos = curPos - gap;
        }
        aList[curPos] = curVal;
    }
}''',
    'shellSort': r'''void shellSort(vector<int>& aList) {
    int sublistCount = aList.size() / 2;
    while (sublistCount > 0) {
        for (int posStart = 0; posStart < sublistCount; posStart++) {
            gapInsertionSort(aList, posStart, sublistCount);
        }
        cout << "After increments of size " << sublistCount << " the list is ";
        printl(aList);
        sublistCount = sublistCount / 2;
    }
}''',
    'mergeSort': r'''void mergeSort(vector<int>& aList) {
    cout << "Splitting ";
    printl(aList);
    if (aList.size() > 1) {
        int mid = aList.size() / 2;
        vector<int> leftHalf(aList.begin(), aList.begin() + mid);
        vector<int> rightHalf(aList.begin() + mid, aList.end());
        mergeSort(leftHalf);
        mergeSort(rightHalf);
        unsigned i = 0, j = 0, k = 0;
        while (i < leftHalf.size() && j < rightHalf.size()) {
            if (leftHalf[i] <= rightHalf[j]) { aList[k] = leftHalf[i]; i++; }
            else { aList[k] = rightHalf[j]; j++; }
            k++;
        }
        while (i < leftHalf.size()) { aList[k] = leftHalf[i]; i++; k++; }
        while (j < rightHalf.size()) { aList[k] = rightHalf[j]; j++; k++; }
    }
    cout << "Merging ";
    printl(aList);
}''',
    'partition': r'''int partition(vector<int>& aList, int first, int last) {
    int pivotVal = aList[first];
    int leftMark = first + 1;
    int rightMark = last;
    bool done = false;
    while (!done) {
        while (leftMark <= rightMark && aList[leftMark] <= pivotVal) leftMark++;
        while (leftMark <= rightMark && aList[rightMark] >= pivotVal) rightMark--;
        if (rightMark < leftMark) done = true;
        else swap(aList[leftMark], aList[rightMark]);
    }
    swap(aList[first], aList[rightMark]);
    return rightMark;
}''',
    'quickSortHelper': r'''void quickSortHelper(vector<int>& aList, int first, int last) {
    if (first < last) {
        int split = partition(aList, first, last);
        printl(aList);
        quickSortHelper(aList, first, split - 1);
        quickSortHelper(aList, split + 1, last);
    }
}''',
    'quickSort': r'''void quickSort(vector<int>& aList) {
    quickSortHelper(aList, 0, aList.size() - 1);
}''',
    'partitionDesc': r'''int partitionDesc(vector<int>& aList, int first, int last, bool descending) {
    int pivotVal = aList[first];
    int leftMark = first + 1;
    int rightMark = last;
    bool done = false;
    while (!done) {
        if (descending) {
            while (leftMark <= rightMark && aList[leftMark] >= pivotVal) leftMark++;
            while (leftMark <= rightMark && aList[rightMark] <= pivotVal) rightMark--;
        } else {
            while (leftMark <= rightMark && aList[leftMark] <= pivotVal) leftMark++;
            while (leftMark <= rightMark && aList[rightMark] >= pivotVal) rightMark--;
        }
        if (rightMark < leftMark) done = true;
        else swap(aList[leftMark], aList[rightMark]);
    }
    swap(aList[first], aList[rightMark]);
    return rightMark;
}''',
    'quickSortHelperDesc': r'''void quickSortHelperDesc(vector<int>& aList, int first, int last, bool descending) {
    if (first < last) {
        int split = partitionDesc(aList, first, last, descending);
        quickSortHelperDesc(aList, first, split - 1, descending);
        quickSortHelperDesc(aList, split + 1, last, descending);
    }
}''',
    'quickSortDesc': r'''void quickSortDesc(vector<int>& aList, bool descending = false) {
    quickSortHelperDesc(aList, 0, aList.size() - 1, descending);
}''',
    'binarySearch': r'''// prints how far the midpoint moves at every probe
bool binarySearch(const vector<int>& aList, int item) {
    int first = 0;
    int last = static_cast<int>(aList.size()) - 1;
    while (first <= last) {
        int midpoint = (first + last) / 2;
        cout << midpoint - first << endl;
        if (aList[midpoint] == item) return true;
        else if (item < aList[midpoint]) last = midpoint - 1;
        else first = midpoint + 1;
    }
    return false;
}''',
    'binarySearchRecRange': r'''// Index bounds keep each recursive step O(1); no sub-vector is copied.
bool binarySearchRecRange(const vector<int>& aList, int item,
                          int first, int last) {
    if (first > last) return false;
    int midpoint = first + (last - first) / 2;
    cout << aList[midpoint] << endl;
    if (aList[midpoint] == item) return true;
    if (item < aList[midpoint]) {
        return binarySearchRecRange(aList, item, first, midpoint - 1);
    }
    return binarySearchRecRange(aList, item, midpoint + 1, last);
}''',
    'binarySearchRec': r'''// Preserve the original two-argument entry point used by the course examples.
bool binarySearchRec(const vector<int>& aList, int item) {
    return binarySearchRecRange(aList, item, 0,
                                static_cast<int>(aList.size()) - 1);
}''',
}
