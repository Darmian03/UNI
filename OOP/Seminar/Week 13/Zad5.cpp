#include <iostream>

int* add(int* arr, int size, int newElement){
    int *array = new int[size+1];
    for(int i = 0; i < size; i++){
        array[i] = arr[i];
    }
    array[size] = newElement;
    return array;
}

int main(){
    int size = 0;
    std::cin >> size;
    int *arr = new int[size];

    for(int j = 0; j < size; j++){
        std::cin >> arr[j];
    }

    int *array = add(arr, size, 9);

    for(int j = 0; j <= size; j++){
        std::cout << array[j];
    }

    delete[] arr;
    delete[] array;
}