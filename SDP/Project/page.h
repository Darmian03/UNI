#pragma once
#include <string>

class Page
{
    private:
    std::string url;
    std::string content;

    public:    
    Page(const std::string&, const std::string&);

    std::string getUrl();

    std::string getContent();

    bool operator==(const Page&);

    bool operator!=(const Page&);

    Page& operator=(const Page&);
};