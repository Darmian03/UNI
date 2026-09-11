#include <iostream>

int main()
{
    int n = 0;
    std::cin >> n;

    int arr[100] = {};

    for(int i = 0; i < n; i++){
        int x;
        std::cin >> x;
        arr[i] = x;
    }

    for(int i = 0; i < n; i++){
        int index = 0;
        for(int j = i+1; j <n; j++){
            if(arr[i] > arr[j]){
                index ++;
            }
        }
        arr[i] = index;
    }

    for(int i = 0; i < n; i++){
        std::cout << arr[i] << " ";
    }
}