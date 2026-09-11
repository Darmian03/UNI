#include <iostream>

int sum(int n[], int size);

int main(){
    int n[] = {1,4,7,2,9,4};
    int size = sizeof(n)/sizeof(n[0]);

    std::cout << sum(n, size-1);
}

int sum(int n[], int size){
    if(size<0){
        return 0;
    }
    return *(n+size) + sum(n, size-1);
}