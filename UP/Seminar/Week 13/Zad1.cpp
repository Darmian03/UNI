#include <iostream>

int main(){
    int n;
    std::cin>>n;

    int *arr = new int[n];

    for(int i = 0; i < n; i++){
        std::cin >> arr[i];
    }

    for(int j = 0; j < n; j++){
        std::cout << arr[j];
    }

    delete[] arr;
}