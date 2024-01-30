import requests
import datetime
import pandas as pd
import os
import time

news_api_url = "https://content.guardianapis.com/search"
api_key = os.getenv('NEWS_API_KEY')


def get_articles(query_list,
                 from_date=(datetime.datetime.now() - datetime.timedelta(
                     days=100)),
                 to_date=datetime.datetime.now()):
    """

    This is a function that returns the articles related to a list of queries
    (keywords) from the guardian api. It returns a dataframe with the articles

    Args:
        query_list (list): list of queries for the articles e.g. ['brexit',
                                                                    'elections']
        from_date (datetime): date from which to start the search
        to_date (datetime): date to which to end the search
    """

    results = []
    """
    generating a date range instead of the api page numbers,
    because there is a limit to the max page number that you can query
    (the api doesn't allow you to query page numbers higher than 10k or so)
    using a date range overcomes that issue)
    """
    dates = [from_date + datetime.timedelta(days=i) for i in range(
        (to_date - from_date).days + 1)]

    # query all the words that are in the search query
    for query in query_list:
        start_date_api = dates[0].strftime('%Y-%m-%d')
        # initial values for the loop to start
        for i in dates[1:]:
            end_date_api = i.strftime('%Y-%m-%d')
            url_params = {
                "api-key": api_key,
                "q": query,
                'page-size': 100,
                'show-fields': 'wordcount',
                'from-date': start_date_api,
                'to-date': end_date_api,
            }

            response = requests.get(news_api_url, params=url_params)
            data = response.json()

            # append article to df list 
            articles = data['response']['results']
            df = pd.DataFrame(articles)

            # clean up the word  count
            df['wordcount'] = df.apply(lambda row: row['fields']['wordcount'],
                                       axis=1)
            df.rename(columns={'wordcount': 'Wordcount'}, inplace=True)
            df.drop(columns=['fields'], inplace=True)

            results.append(df)

            start_date_api = end_date_api

            # sleep 30 seconds to not exceed api rates (kinda annoying)
            time.sleep(30)

    results = pd.concat(results)
    results = results.drop_duplicates(subset='id').reset_index()
    results.drop(columns=['index'], inplace=True)

    # sort by publication date
    results['webPublicationDate'] = pd.to_datetime(results['webPublicationDate'])
    results = results.sort_values(by='webPublicationDate', ascending=False)

    return results


def aggregate_data(articles_file_name: str):

    df = pd.read_csv(articles_file_name)

    # get monthly number of articles by pillarName
    df['webPublicationDate'] = pd.to_datetime(df['webPublicationDate'])
    df['month'] = df['webPublicationDate'].dt.to_period('M')
    df['count'] = 1
    df = df.groupby(['pillarName', 'month']).count().reset_index()
    df = df[['count', 'month', 'pillarName']]
    df.sort_values(by='month', inplace=True)

    return df


if __name__ == "__main__":
    df = get_articles(["brexit", "elections"])
    df.to_csv("articles.csv", index=False)

    df = aggregate_data("articles.csv")
    df.to_csv("articles_aggregated.csv", index=False)