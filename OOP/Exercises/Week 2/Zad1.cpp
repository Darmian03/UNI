#include <iostream>

int main()
{
    int friendsnum;
    std::cout << "Enter number of friends: ";
    std::cin >> friendsnum;

    for(int i = 1; i <=friendsnum; i++){
        std::string name;
        std::cout << "Name:";
        std::cin >> name;
        int age;
        std::cout << "Age:";
        std::cin >> age;
        if(age < 18){
            std::cout << "Sorry " << name <<" you can't enter" << std::endl;
        }
        else{
            "You can proceed.";
        }
    }
    return 0;
}