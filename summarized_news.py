from gensim.summarization.summarizer import summarize
# from gensim.summarization.textcleaner import split_sentences
import re

# extract selected company's news header
def summarized_multiple_news(company_news, n_sen):
    # replace \. with space
    # sort by time (latest news first)
    company_news.sort_values(by = 'time', ascending = False)
    company_news.loc[:, 'header_clean'] = [re.sub('\.|\?', ' ', h) for h in company_news.header].copy()
    company_headers = company_news['header_clean'].tolist()
    company_headers_all = '\n'.join(company_headers)
    # summaize headers
    rt = n_sen / len(company_news)
    summarized_headers = summarize(company_headers_all, ratio = rt, split = True)
    
    if len(summarized_headers) == 0:
        summarized_headers = company_headers_all.copy()
    summarized_news_df = company_news[company_news.header_clean.isin(summarized_headers)]
    summarized_news_df.drop_duplicates(subset = ['header', 'header_clean'],inplace = True)
    return summarized_news_df