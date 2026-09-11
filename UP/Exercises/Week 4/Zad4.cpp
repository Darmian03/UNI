#include <iostream>

int primeNumbers(int n);

int main()
{
    int n;
    std::cin >> n;

    std::cout << primeNumbers(n);
}

int primeNumbers(int n){
    int count = 2;

    if (n>2){
        for(int i = 3; i <= n; i++){
            bool prime = true;
            for (int j = 2; j < i; j++) {
                if (i % j == 0) {
                    prime = false;
                    break;
                }
            }
            if(prime == true){
                count++;
            }
        }
        return count;
    }
    else if(n==2){
        return 2;
    }
    else{
        return 1;
    }
}