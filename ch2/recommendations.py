# A dictionary of movie critics and their ratings of a small
# set of movies

critics={
	'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
	'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5}, 
	'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0}, 'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
	'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0}, 
	'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
}

# A function to calculate similarity score using Euclidean distance
from math import sqrt

def sim_distance(prefs, person1, person2):
	# Get the list of shared_items
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1

	if len(si) == 0: return 0

	sum_of_squares = sum([pow((prefs[person1][item] - prefs[person2][item]),2) for item in si])
	
	return 1/(1+sqrt(sum_of_squares))


# Pearson Correlation #by myself
from numpy import corrcoef

def sim_pearson(prefs, p1,p2):
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item]=1

	if len(si)==0: return 0
	
	# make two vectors for calculating P-corr
	a=[]
	b=[]
	for item in si:
		a.append(prefs[p1][item])
		b.append(prefs[p2][item])
	r = corrcoef(a,b)[0,1]
	return r




# Top Match Function using Pearson Corr as default
def topMatches(prefs, person, n=5, similarity=sim_distance):
	scores=[(similarity(prefs, person, other),other) for other in prefs if other != person]

	#sort
	scores.sort()
	scores.reverse()
	return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:
		if other == person: continue
		sim=similarity(prefs, person, other)

		#ignore scores of 0 or lower
		if sim <= 0: continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item] == 0:
				totals.setdefault(item,0)
				totals[item] += prefs[other][item] * sim
				simSums.setdefault(item,0)
				simSums[item] += sim

	# create the normalized list
	rankings=[(total/simSums[item], item) for item, total in totals.items()]
	rankings.sort()
	rankings.reverse()
	return rankings


# do the reverse from person-movie to movie-person
def transformPrefs(prefs):
	result={}
	
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})

			result[item][person]=prefs[person][item]
	return result


