#include <iostream>

void replace(int array[], int size, int find, int rep);

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

    int find, rep;
    std::cout << "Find: ";
    std::cin >> find;
    std::cout << "Replace: ";
    std::cin >> rep;

    replace(arr,size,find,rep);
}

void replace(int array[], int size, int find, int rep){
    for(int i = 0; i <size; i++){
        if(array[i] == find){
            array[i] = rep;
        }
    }

    for(int i = 0; i < size; i++){
        std::cout << array[i] << " ";
    }
}