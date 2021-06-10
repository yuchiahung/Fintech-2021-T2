from summarizer import Summarizer
from transformers import AutoTokenizer, AutoConfig, AutoModel
import re

# extract selected company's news header
def summarized_multiple_news(company_news, n_sen):
    # replace \. with space
    # sort by time (latest news first)
    company_news.sort_values(by = 'time', ascending = False)
    company_news.loc[:, 'header_clean'] = [re.sub('\.', ' ', h) for h in company_news.header].copy()
    company_headers = '. '.join(company_news['header_clean'].tolist())
    # summaize headers
    modelName = "bert-base-uncased" # lower-cased
    custom_config = AutoConfig.from_pretrained(modelName)
    custom_config.output_hidden_states=True
    custom_tokenizer = AutoTokenizer.from_pretrained(modelName)
    custom_model = AutoModel.from_pretrained(modelName, config=custom_config)
    model = Summarizer(custom_model=custom_model, custom_tokenizer=custom_tokenizer)
    summarized_headers = model(company_headers, num_sentences = n_sen)[:-1].split('. ')
    summarized_news_df = company_news[company_news.header_clean.isin(summarized_headers)]
    summarized_news_df.drop_duplicates(subset = ['header', 'header_clean'],inplace = True)
    return summarized_news_df