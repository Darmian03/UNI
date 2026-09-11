#include <iostream>

void count(int* arr, int size, int find);

int main()
{
    int arr[] = {45, 3, 24, 9, 29, 45, 4, 3, 12, 40};
    int size = sizeof(arr) / sizeof(arr[0]);
    int* start = arr;

    int find = 0;
    std::cin >> find;

    count(start, size, find);
}

void count(int* arr, int size, int find){
    int occurences = 0;

    for(int i=0; i<size; i++){
        if(find == *(arr + i)){
            occurences++;
        }
    }

    std::cout << occurences;
}