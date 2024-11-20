from functions import retriever

result = retriever("용산구", 10)
print(len(result))
for i in result:
    print(i.metadata['title'])
    print(i.metadata['article_date'])
    print(i.metadata['company'])
    print(i.metadata['url'])