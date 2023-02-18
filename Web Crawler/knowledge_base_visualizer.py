import pickle


if __name__ == '__main__':
    # unpickle the knowledge base and summarize it
    with open('./knowledge_base.pickle', 'rb') as f:
        knowledge_base = pickle.load(f)

    for keyword in knowledge_base:
        print('Keyword: {}'.format(keyword))
        print('Number of files: {}'.format(len(knowledge_base[keyword])))
        # print a sampling of the files
        for file in knowledge_base[keyword][:5]:
            # print the first 10 words of the file
            print(' '.join(file[:10]))
        print('----------------------------------------------------------------------------')