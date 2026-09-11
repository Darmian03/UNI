#include <iostream>

int main()
{
    int n = 0;
    std::cin >> n;

    char arr[n] = {};

    for(int i = 0; i < n; i++){
        char x;
        std::cin >> x;
        arr[i] = x;
    }

    for(int i = 0; i < n; i++){
        if(arr[i]>=65 && arr[i]<=90){
            std::cout << arr[i] << " ";
        }
    }
}