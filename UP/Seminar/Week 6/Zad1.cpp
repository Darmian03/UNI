#include <iostream>

bool contains(int array[], int size, int elem);

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

    int elem;
    std::cout << "Element: ";
    std::cin >> elem;

    std::cout << contains(arr, size, elem);
}

bool contains(int array[], int size, int elem){
    for(int i = 0; i <size; i++){
        if(elem == array[i]){
            return true;
            break;
        }
    }
    return false;
}