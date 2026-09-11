#include <iostream>

int* createArray(int size){
    int *arr = new int[size];
    for(int i = 0; i < size; i++){
        std::cin >> arr[i];
    }

    return arr;
}

int main(){
    int n;
    std::cin >> n;
    
    int *arr = createArray(n);

    for(int j = 0; j < n; j++){
        std::cout << arr[j];
    }

    delete[] arr;
}