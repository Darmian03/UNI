#include <list>
#include "page.cpp"

class Tab
{
    private:
    std::list<Page> history;
    std::_List_iterator<Page> currentPage;

    public:
    Tab();

    Tab(const Page&);

    void back();

    void forward();

    void visit(const Page&);

    Page& getPage();
};