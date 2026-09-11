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

        for(int i = 0; i < n; i++){
            if(arr[i]%2 == 0){
                std::cout << arr[i] << " ";
            }
        }
    }
}