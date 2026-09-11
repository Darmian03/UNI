#include <iostream>
#include <cstdlib>

int main(){
    int n;
    std::cout << "Please enter a limit: ";
    std::cin >> n;

    int counter = 0;
    int rnd = std::rand() % n;
    int a = 0;
    std::cout << rnd;

    if(n>=1){
        while(a == 0){
            int x;
            std::cout << "Please enter a number: ";
            std::cin >> x;
            counter++;

            if(rnd>x){
                std::cout << "Your number is less than the generated number." << std::endl;
            }
            else if(rnd<x){
                std::cout << "Your number is greater than the generated number." << std::endl;
            }
            else if(rnd == x){
                std::cout << "Congrats! You guessed the number! You needed " << counter << " tries to guess it!";
                a++;
            }
        }
    }
    else{
        std::cout << "Please enter a positive number!";
    }
    return 0;
}