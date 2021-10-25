from reddit.reddit_client import reddit_client

makeupCompanies = {} #Dictonary used to store <company name, list of posts>
redditPosts = [] #Contains all posts read in by file.

#Inherited class from reddit_client.py
class MUAontheCheap(reddit_client):
    pass


    #Pre-Condition : Valid MakeupCompanies.txt and MUAhot.txt
    #Post-Condition : None
    #Purpose of the function is to populate a list of makeup companies
    #and reddit posts.
    def PopulateCompanies(self):
        companyList = open("MakeupCompanies.txt", "r")
        for companyName in companyList: 
            companyName = companyName.replace("\n","")
            makeupCompanies[companyName] = []; #initalize company name and count 
        
        makeupCompanies["other"] = [] #used to catch all companies not found in text file.
        companyList.close()
        redditList = open("MUAhot.txt", "r")

        for redditPost in redditList:
            redditPost = redditPost.replace("\n","")
            redditPosts.append(redditPost) #all possible reddit posts
        redditList.close()

    #Pre-Condition : None
    #Post-Condition : Returns a dictonary of <string, list>. The key represents the company
    #and the value represents the list of posts correlated with company.
    #Purpose of this function is to compare and count companies found in a 
    def CompanyCount(self):     
        self.PopulateCompanies()
        printOther = True #Used to debugging purposes. Prints companies not captured.
        
        for postTitle in redditPosts:
            foundCompany = False
            for companyName in makeupCompanies:
                 #Iterate through all potential companies. Reason we dont break is incase
                 #there are multiple companies in title.
                if companyName.lower() in postTitle.lower():
                    makeupCompanies[companyName].append(postTitle)
                    foundCompany = True
            if(not foundCompany):
                makeupCompanies["other"].append(postTitle)
       
 
        """
        #A formatted way to see the amount of posts correlated to a company.
        for companyName in makeupCompanies:
            print(companyName + " : " + str(len(makeupCompanies[companyName])))

        if(printOther):
            print("Printing Missed Companies \n")
            for unknownCompany in makeupCompanies["other"]:
                print(unknownCompany)
        """

        return makeupCompanies






