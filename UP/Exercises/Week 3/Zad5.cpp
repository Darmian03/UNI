#include <iostream>
#include <cmath>

int main()
{
    int a,b,sum;
    std::cin >> a;
    std::cin >> b;


    if(a<b){
        while(a<=b){
            sum += a;
            a++;
        }
    }
    else{
        while(b<=a){
        sum += b;
        b++;
        }
    }
    std::cout << sum;
    return 0;
}