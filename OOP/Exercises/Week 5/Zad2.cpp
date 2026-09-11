#include <iostream>

int main()
{
    int n = 0;
    std::cin >> n;
    if(n<20){
        int arr[n] = {};

        for(int i = 0; i < n; i++){
            int x = 0;
            std::cin >> x;
            arr[i] = x;
        }

        int sum = 1;
        for(int i = 0; i < n; i++){
            sum *= arr[i];
        }

        std::cout << sum;
    }
}