#include <iostream>

int main()
{
    int a,b,c;
    std::cin >> a;
    std::cin >> b;
    std::cin >> c;

    if(a>b){
        if(a>c){
            if(c>b){
                std::cout << a << " " << c << " " << b;
            }
            else{
                std::cout << a << " " << b << " " << c;
            }
        }
        else{
            std::cout << c << " " << a << " " << b;
        }
    }
    else{
        if(b>c){
            if(c>a){
                std::cout << b << " " << c << " " << a;
            }
            else{
                std::cout << b << " " << a << " " << c;
            }
        }
        else{
            std::cout << c << " " << b << " " << a;
        }
    }
    return 0;
}