#include <iostream>

void populateArr(int* start, int size);
void printArr(int* start, int size);

int main()
{
    int arr[] = {1, 2, 3, 4, 5};
    int size = sizeof(arr) / sizeof(arr[0]);

    int* start = arr;

    populateArr(start, size);
    printArr(start, size);
}

void populateArr(int* start, int size){
    for(int i = 0; i<size; i++){
        int x = 0;
        std::cin >> *(start + i);
    }
}

void printArr(int* start, int size){
    for(int i = 0; i<size; i++){
        std::cout << *(start + i);
    }
}