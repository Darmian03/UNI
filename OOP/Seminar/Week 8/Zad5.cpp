#include <iostream>

void capitalizeChars (char* word);

int main()
{
    char arr[100];

    std::cin >> arr;
    char* word = arr;

    capitalizeChars(word);

    for(int i=0; i<100; i++){
        std::cout << *(word + i);
    }
}

void capitalizeChars (char* word){
    for(int i=0; i < 100; i++){
        if(*(word + i) >= 'a' && *(word +i) <= 'z'){
            *(word + i) -= 32;
        }
    }
}