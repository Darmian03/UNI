#include <iostream>

int main(){
    int x;

    std::cout << "Enter a positive number:";
    std::cin >> x;

    std::string revx = "";
    std::string x1 = std::to_string(x);

    if(x>0){
        while(x>0){
            int a = x%10;
            revx += std::to_string(a);
            x/=10;
        }

        if(x1==revx){
            std::cout << "True";
        }
        else{
            std::cout << "False";
        }
    }
    else{
        std::cout << "Please enter a positive number!";
    }
}