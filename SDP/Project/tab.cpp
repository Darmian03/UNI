#include <iostream>
#include "tab.h"

Tab::Tab()
{
    currentPage = history.begin();
}

Tab::Tab(const Page& page)
{
    history.push_back(page);
    currentPage = history.begin();
    std::cout << currentPage->getContent() << std::endl;
}

void Tab::back()
{
    if(history.empty()){
        return;
    }

    if(currentPage == history.begin()){
        std::cout << currentPage->getContent() << std::endl;
        return;
    }

    --currentPage;
    std::cout << currentPage->getContent() << std::endl;
}

void Tab::forward()
{
    if(history.empty()){
        return;
    }
    
    if(currentPage == --history.end()){
        std::cout << currentPage->getContent() << std::endl;
        return;
    }

    ++currentPage;
    std::cout << currentPage->getContent() << std::endl;
}

void Tab::visit(const Page& newPage)
{
    while(currentPage != --history.end() && !history.empty()){
        history.pop_back();
    }

    history.push_back(newPage);
    currentPage = --history.end();

    std::cout << currentPage->getContent() << std::endl;
}

Page& Tab::getPage()
{
    if(history.empty()){
        throw std::invalid_argument("Error! The current tab doesn't have a opened page.");
    }
    return *currentPage;
}