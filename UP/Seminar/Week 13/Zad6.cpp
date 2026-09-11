#include <iostream>

int* insertAt(int* arr, int size, int newElement, int index){
    int *array = new int[size+1];

    bool smth = true;
    for(int i = 0; i < size; i++){
        if(i == index-1){
            smth = false;
            array[i] = newElement;
        }
        if(smth){
            array[i] = arr[i];
        }
        else{
            array[i+1] = arr[i];
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

    int *array = insertAt(arr, size, 9, 4);

    for(int j = 0; j <= size; j++){
        std::cout << array[j];
    }

    delete[] arr;
    delete[] array;
}