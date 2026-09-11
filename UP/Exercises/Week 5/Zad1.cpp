#include <iostream>

int main()
{
    int n = 0;
    std::cin >> n;

    int arr[n] = {};

    for(int i = 0; i < n; i++){
        int x = 0;
        std::cin >> x;
        arr[i] = x;
    }

    for(int i = 0; i < n; i++){
        std::cout << arr[i] << " ";
    }
}