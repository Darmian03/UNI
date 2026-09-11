#include <iostream>

char* concat(char* first, char* second){
    int size1 = sizeof(first)/first[0];
    int size2 = sizeof(second)/second[0];

    char *result = new char[size1 + size2 - 1];
    for(int i = 0; i < size1; i++){
        result[i] = first[i];
    }

    for(int i = 0; i < size2; i++){
        result[size1 + i] = second[i];
    }

    return result;
}

int main(){
    int size1, size2;

    std::cin >> size1;
    std::cin >> size2;

    char *arr1 = new char[size1];
    char *arr2 = new char[size2];

    std::cin >> arr1;
    std::cin >> arr2;

    char *arr = concat(arr1, arr2);

    for(int j = 0; j < size1+size2; j++){
        std::cout << arr[j];
    }

    delete[] arr;
}