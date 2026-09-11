#include <iostream>
#include <climits>
#include <cmath>

int main()
{
    int count;
    std::cout << "Enter how many numbers you will enter:";
    std::cin >> count;

    double sum = 0;
    int biggest = INT_MIN;
    int lowest = INT_MAX;

    for(int i = 0; i < count; i++){
        int number;
        std::cin >> number;

        sum += number;

        if(number>biggest){
            biggest = number;
        }else if(number<lowest){
            lowest = number;
        }
    }

    double avr = sum/count;

    std::cout << "Min = " << lowest << std::endl;
    std::cout << "Max = " << biggest << std::endl;
    std::cout << "Average = " << printf("%.1f",avr) << std::endl;
    return 0;
}