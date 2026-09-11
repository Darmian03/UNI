#include <iostream>

char* nextSentence(char* text, int size);

int main()
{
    char arr[100];
    int size = sizeof(arr)/sizeof(*arr);

    std::cin >> arr;
    char* text = arr;

    std::cout << nextSentence(text, size);
}

char* nextSentence(char* text, int size){
    for(int i=0; i<size; i++){
        if(*(text + i) == '.'){
            text += i;
            return text;
            break;
        }
    }
}