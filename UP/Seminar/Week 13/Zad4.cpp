#include <iostream>

int* toSet(int* arr, int size, int& setSize){
    setSize = size;

    int *array = new int[setSize];

    int index = 0;

    for(int i = 0; i < size; i++){
        bool smth = true;
        for(int j = 0; j < i; j++){
            if(arr[i] == arr[j]){
                smth = false;
            }
        }
        if(smth){
            array[index] = arr[i];
            index++;
        }
        else{
            setSize--;
        }
    }

    return array;
}

int main(){
	int arr[] = {1, 2, 1, 3, 4, 2, 8, 8, 9};
	int setSize = 0;
	int *set = toSet(arr,9,setSize);

    std::cout << setSize;

    for(int j = 0; j < setSize; j++){
        std::cout << set[j];
    }

    delete[] set;
}