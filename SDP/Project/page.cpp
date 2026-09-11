#include "page.h"

Page::Page(const std::string& _url, const std::string& _content): url(_url), content(_content){}

std::string Page::getUrl()
{
    return url;
}

std::string Page::getContent()
{
    return content;
}

bool Page::operator==(const Page& other)
{
    return url == other.url && content == other.content;
}

bool Page::operator!=(const Page& other)
{
    return url != other.url || content != other.content;
}

Page& Page::operator=(const Page& other)
{
    if(this != &other){
        this->url = other.url;
        this->content = other.content;
    }

    return *this;
}