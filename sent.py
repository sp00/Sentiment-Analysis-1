import numpy as np
import twitter 

def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() 
    
    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])

    return happy_log_probs, sad_log_probs

def classifySentiment(words, happy_log_probs, sad_log_probs):
    happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
    sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]

    tweet_happy_log_prob = np.sum(happy_probs)
    tweet_sad_log_prob = np.sum(sad_probs)

    prob_happy = np.reciprocal(np.exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
    prob_sad = 1 - prob_happy

    return prob_happy, prob_sad

def main():
	
	api = twitter.Api()
	tweets = api.GetSearch(term="#sport", per_page=100, page=1)
	happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')

	for s in tweets: 
		tweet1 = s.text.split(" ")
		tweet1_happy_prob, tweet1_sad_prob = classifySentiment(tweet1, happy_log_probs, sad_log_probs)
		print "The probability that tweet1 (", tweet1, ") is happy is ", tweet1_happy_prob, "and the probability that it is sad is ", tweet1_sad_prob

if __name__ == '__main__':
    main()
