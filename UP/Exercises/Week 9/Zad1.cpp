#include <iostream>

void swap(int* a, int* b);

int main()
{
    int a = 0;
    std::cin >> a;
    int b = 0;
    std::cin >> b;

    std:: cout << &a << " " << &b << std::endl;

    swap(&a, &b);
}

void swap(int* a, int* b){
    int* c = a;
    a = b;
    b = c;

    std:: cout << a << " " << b << std::endl;
}