#include <iostream>

int main()
{
    int a;
    std::string characters[26] = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"};

    std::cout << "Enter a number:";
    std::cin >> a;

    if(a>0 && a<27)
    {
       std::cout << "Your character is:" << characters[a-1];
    }else {
        std::cout << "Please enter a number between 1 and 26!";
    }
    return 0;
}