#include <iostream>
#include <cmath>

int main()
{
    double money;
    double whiskey;
    double nargile;
    int people;

    std::cout << "Money that Misho has:";
    std::cin >> money;
    std::cout << "Price of the whiskey:";
    std::cin >> whiskey;
    std::cout << "Price of the nargile:";
    std::cin >> nargile;
    std::cout << "Number of people:";
    std::cin >> people;
    if(money < whiskey/people){
        std::cout << "Bruh, you don't have money even for the alcohol.";
    }
    else{
        money = money - std::ceil(whiskey/people);
        if(money <= 0){
            std::cout << "Lmao, you don't have money.";
        }
        else{
            if(money >= nargile){
                std::cout << "True.";
            }
            else{
                std::cout << "False";
            }
        }
    }
    return 0;
}