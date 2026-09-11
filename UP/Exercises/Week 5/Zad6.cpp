#include <iostream>

int main()
{
    int n = 0;
    std::cin >> n;
    if(n>0 && n<20){
        int arr[n] = {};

        for(int i = 0; i < n; i++){
            int x = 0;
            std::cin >> x;
            arr[i] = x;
        }

        int sum = 0;
        for(int i = 0; i < n; i++){
            if(i%3 == 0){
                sum += arr[i];
            }
        }

        std::cout << sum;
    }
}