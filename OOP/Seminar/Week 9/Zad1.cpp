#include <iostream>

int* findBiggest(int* start, int* end);

int main()
{
    int arr[] = {2, 9, 4, 6, 10, 13, 2, 3, 5, 9};
    int size = sizeof(arr)/ sizeof(arr[0]);

    int* start = arr;
    int* end = arr + size - 1;

    std::cout << *findBiggest(start, end);
}

int* findBiggest(int* start, int* end){
    int *max = start;

    while(start <= end){
        if(*start > *max){
            max = start;
        }
        start++; 
    }

    return max;
}