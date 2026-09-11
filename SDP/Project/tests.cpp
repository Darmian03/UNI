#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "slow-web.cpp"


TEST_CASE("testing class Page")
{
    Page page("test.com", "Testing");
    Page otherPage("othertest.com", "Other Test");

    CHECK(page.getUrl() == "test.com");
    CHECK(page.getContent() == "Testing");
    CHECK(page != otherPage);

    page = otherPage;

    CHECK(page == otherPage);
}

TEST_CASE("testing class Tab")
{
    Page page1("test1.com", "Testing 1");
    Page page2("test2.com", "Testing 2");
    Page page3("test3.com", "Testing 3");
    Tab tab;
    tab.back();
    tab.visit(page1); //Testing 1

    CHECK(tab.getPage() == page1);

    tab.back(); //Testing 1

    CHECK(tab.getPage() == page1);

    tab.forward(); //Testing 1

    CHECK(tab.getPage() == page1);

    tab.visit(page2); //Testing 2

    CHECK(tab.getPage() == page2);

    tab.back(); //Testing 1

    CHECK(tab.getPage() == page1);

    tab.forward(); //Testing 2

    CHECK(tab.getPage() == page2);

    tab.back(); //Testing 1
    tab.visit(page3); //Testing 3

    CHECK(tab.getPage() == page3);

    tab.forward(); //Testing 3

    CHECK(tab.getPage() == page3);

    tab.back(); //Testing 1

    CHECK(tab.getPage() == page1);

    std::cout << std::endl;
}

TEST_CASE("testing class Browser")
{
    Page page1("test1.com", "Testing 1");
    Page page2("test2.com", "Testing 2");
    Page page3("test3.com", "Testing 3");
    Page page4("test4.com", "Testing 4");
    Page page5("test5.com", "Testing 5");
    Page page6("test6.com", "Testing 6");

    Browser browser;
    browser.back(); //Error! The current tab doesn't have a opened page.
    browser.closeTab(); //
    browser.go(page1); //Testing 1
    browser.go(page2); //Testing 2
    browser.bookmark("pg2", "TestBookmark"); //Done!
    browser.back(); //Testing 1
    browser.viewHistory(); //test1.com,test2.com,test1.com
    browser.clearHistory(); //History cleared.
    browser.forward(); //Testing 2
    browser.newTab(page3); //Testing 3
    browser.bookmark("pg3", ""); //Done!
    browser.switchTab(0); //Testing 2
    browser.closeTab(); //Testing 3
    browser.viewHistory(); //test3.com,test2.com
    browser.go(page2); //Testing 2
    browser.bookmark("pg2", ""); //Done!
    browser.historyRemove(page2.getUrl()); //Done!
    browser.viewHistory(); //test3.com
    browser.viewBookmarks(""); //pg3,pg2
    browser.viewBookmarks("TestBookmark"); //pg2
    browser.removeBookmark("pg2", ""); //Done!
    browser.viewBookmarks(""); //pg3
    browser.viewBookmarks("Error"); //Error! Folder Error does not exist.
    browser.removeBookmark("pg3", ""); //Done!
    browser.removeBookmark("pg3", "Error"); //Error! Folder Error does not exist!
    browser.viewBookmarks(""); //
    browser.removeBookmark("pg3", ""); //Done!

    std::cout << std::endl;
}

TEST_CASE("testing class Cache")
{
    Cache cache(5);

    cache.putContent("test1.com", "Testing 1");
    cache.putContent("test2.com", "Testing 2");

    CHECK(cache.contains("test1.com"));
    CHECK(!cache.contains("test3.com"));
    CHECK(cache.getContent("test2.com") == "Testing 2");

    cache.putContent("test3.com", "Testing 3");
    cache.putContent("test4.com", "Testing 4");
    cache.putContent("test5.com", "Testing 5");
    cache.putContent("test6.com", "Testing 6");
    Cache other(5);
    other = cache;

    CHECK(!cache.contains("test1.com"));
    CHECK(other.contains("test3.com"));
    CHECK(other.contains("test5.com"));

    //cache.getContent("test1.com"); -- това хвърля грешка, понеже test1.com не е в cache. Предвидено е да става, и няма да влизаме в случай, в който да не е вътре
}

TEST_CASE("testing class SlowWeb")
{
    SlowWeb browser;

    browser.command("back"); //Error! The current tab doesn't have a opened page.
    browser.command("forward"); //Error! The current tab doesn't have a opened page.
    browser.command("go test1.com"); //404: Not Found
    browser.command("go www.wikipedia.com"); // Welcome to Wikipedia!
    browser.command("bookmark wiki"); //Done!
    browser.command("back"); //Welcome to Wikipedia!
    browser.command("newtab www.google.com"); //Welcome to Google!
    browser.command("bookmark google google");
    browser.command("newtab test1.com"); //404: Not Found
    browser.command("something"); //Error! Invalid command.
    browser.command("viewhistory"); //www.google.com,www.wikipedia.com
    browser.command("clearhistory"); //History cleared.
    browser.command("switchtab 0"); //Welcome to Wikipedia!
    browser.command("closetab"); //Welcome to Google!
    browser.command("viewhistory"); //Huh. There is no history.
    browser.command("go www.maps.com"); //Welcome to Google Maps!
    browser.command("go www.youtube.com"); //Welcome to YouTube!
    browser.command("bookmark you google"); //Done!
    browser.command("viewhistory"); //www.youtube.com,www.maps.com
    browser.command("historyremove www.maps.com"); //Done!
    browser.command("viewhistory"); //www.youtube.com
    browser.command("viewbookmarks google"); //google,you
    browser.command("removebookmark you google"); //Done!
    browser.command("viewbookmarks google"); //google
    browser.command("viewbookmarksp"); //Error! Invalid command.
    browser.command("viewbookmarks"); //wiki
    browser.command("removebookmark wiki"); //Done!
    browser.command("viewbookmarks"); //
}