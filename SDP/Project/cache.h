#include <unordered_map>
#include <string>

class Cache
{
    private:
    struct Node
    {
        std::string url;
        std::string content;
        Node* prev;
        Node* next;

        Node(const std::string&,const std::string&);
    };

    std::unordered_map<std::string, Node*> cache;
    Node *head;
    Node *tail;
    int size;
    int capacity;

    void removeNode(Node*);

    void addNodeToHead(Node*);

    void moveToHead(Node*);

    Node* popTail();

    void cleanup();

    void copy(const Cache&);

    public:
    Cache();

    Cache(const int&);

    Cache(const Cache&);

    ~Cache();

    Cache &operator=(const Cache&);

    bool contains(const std::string&);

    std::string getContent(const std::string&);

    void putContent(const std::string&, const std::string&);
};