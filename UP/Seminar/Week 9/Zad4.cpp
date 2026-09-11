#include <iostream>

int sum(int* a, int* b);

int main()
{
    int arr[] = {2, 9, 4, 6, 10, 13, 2, 3, 5, 9};
    int size = sizeof(arr)/ sizeof(arr[0]);
    int* start = arr;
    int* end = arr + size - 1;

    std::cout << sum(start, end);
}

int sum(int* a, int* b){
    if(a==b){
        return *a;
    }
    else{
        return *a+sum(a+1, b);
    }
}