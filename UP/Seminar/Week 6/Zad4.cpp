#include <iostream>

bool arithmeticProgression(int array[], int size);

int main()
{
    int size = 0;
    std::cin >> size;

    int arr[100] = {};

    for(int i = 0; i < size; i++){
        int x;
        std::cin >> x;
        arr[i] = x;
    }

    std::cout << arithmeticProgression(arr, size);
}

bool arithmeticProgression(int array[], int size){
    int d = array[1] - array[0];

    for(int i = 1; i < size-1; i++){
        if(array[i+1] - array[i] != d){
            return false;
            break;
        }
    }

    return true;
}