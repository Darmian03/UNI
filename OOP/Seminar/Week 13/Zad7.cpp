#include <iostream>

int* resize(int* arr, int size, int newSize){
    int *array = new int[newSize];
    if(size > newSize){
        for(int i = 0; i < newSize; i++){
        array[i] = arr[i];
        }
    }
    else{
        for(int i = 0; i < newSize; i++){
            array[i] = arr[i];
        }
        for(int i = 0; i < newSize - size; i++){
            array[size + i] = 0;
        }
    }

    return array;
}

int main(){
    int size = 0;
    std::cin >> size;
    int *arr = new int[size];

    for(int j = 0; j < size; j++){
        std::cin >> arr[j];
    }

    int newSize = 5;

    int *array = resize(arr, size, newSize);

    for(int j = 0; j < newSize; j++){
        std::cout << array[j];
    }

    delete[] arr;
    delete[] array;
}