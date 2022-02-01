from models.reddit_client import RedditClient

#Inherited class from reddit_client.py
class MUAontheCheapDeal(RedditClient):
    pass
    
    def __init__(self):
        super(MUAontheCheapDeal,self).__init__()
        self.makeupCompanies = {} #Dictonary used to store <company name, list of posts>
        self.redditPosts = [] #Contains all posts read in by file.

    #Pre-Condition : Valid MakeupCompanies.txt and MUAhot.txt
    #Post-Condition : None
    #Purpose of the function is to populate a list of makeup companies
    #and reddit posts.
    def PopulateCompanies(self):
        companyList = open("MakeupCompanies.txt", "r")
        for companyName in companyList: 
            companyName = companyName.replace("\n","")
            self.makeupCompanies[companyName] = []; #initalize company name and count 
        
        self.makeupCompanies["other"] = [] #used to catch all companies not found in text file.
        companyList.close()
        redditList = open("MUAhot.txt", "r")
        for redditPost in redditList:
            redditPost = redditPost.replace("\n","")
            self.redditPosts.append(redditPost) #all possible reddit posts
        redditList.close()

    #Pre-Condition : None
    #Post-Condition : Returns a dictonary of <string, list>. The key represents the company
    #and the value represents the list of posts correlated with company.
    #Purpose of this function is to compare and count companies found in a 
    def CompanyCount(self):    
        """
        #A formatted way to see the amount of posts correlated to a company.
        #printOther = True #Used to debugging purposes. Prints companies not captured.
        for companyName in makeupCompanies:
            print(companyName + " : " + str(len(makeupCompanies[companyName])))

        if(printOther):
            print("Printing Missed Companies \n")
            for unknownCompany in makeupCompanies["other"]:
                print(unknownCompany)
        """
        self.PopulateCompanies()
        
        for postTitle in self.redditPosts:
            foundCompany = False
            for companyName in self.makeupCompanies:
                 #Iterate through all potential companies. Reason we dont break is incase
                 #there are multiple companies in title.
                if companyName.lower() in postTitle.lower():
                    self.makeupCompanies[companyName].append(postTitle)
                    foundCompany = True
            if(not foundCompany):
                self.makeupCompanies["other"].append(postTitle)
     
        return self.makeupCompanies






