from reddit.reddit_client import reddit_client
#Inherited class from reddit_client.py
class MUAontheCheapDeal(reddit_client):
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
        printOther = True #Used to debugging purposes. Prints companies not captured.
        for companyName in self.makeupCompanies:
            print(companyName + " : " + str(len(self.makeupCompanies[companyName])))
        return self.makeupCompanies

    def OldValidateCompany(self):
        redditList = open("Posts.txt", "r", encoding = "utf-8")
        postTitle = ""
        postBody = ""
        readBody = False 
        successPosts = [()]
        failPosts = [()]
        i = 0
        for x in redditList:
            i = i + 1
            if "Title:" in x:
                postTitle = x
            if "Body:" in x:
                start = x.find("://")
                end = x.find(".com")
                for link in range(start, end):
                    postBody += x[link]
                postBody = postBody.replace("://", "")
                postBody = postBody.replace("www.", "")
            if "Url:" in x:
                if "Daily Chat" in postTitle:
                    postBody = ""
                    continue
                if postBody == "":
                    start = x.find("://")
                    end = x.find(".com")
                    for link in range(start, end):
                        postBody += x[link]
                    postBody = postBody.replace("://", "")
                    postBody = postBody.replace("www.", "")
                
                
                if postBody != "" and str(postBody.lower()) in str(postTitle.lower()):
                    successPosts.append((postTitle, postBody))
                else:
                    failPosts.append((postTitle, postBody))
            postBody = ""
        
        print("Correct:" + str(len(successPosts)-1))
        print("Wrong: " + str(len(failPosts)-1))

    def FindDomain(self, textBody : str):
        potentialName = ""
        start = textBody.find("://")
        end = textBody.find(".com")
        for domainName in range(start, end):
            potentialName += textBody[domainName]
        potentialName = potentialName.replace("://", "")
        potentialName = potentialName.replace("www.", "")
        return potentialName

    def ValidateCompany(self, results): #MAKE SURE U USE TYPES 
        fail = open("failPosts.txt", "a")
        postTitle = ""
        companyName = ""
        successPosts = [()]
        failPosts = [()]
        i = 0
        for userSubmission in results:
            if "Daily Chat" in userSubmission.title:
                continue
            postTitle = userSubmission.title
            print("Title: " + postTitle)
            #Post Body
            potenName = self.FindDomain(userSubmission.selftext.replace("\n", ""))
            if potenName.lower() in postTitle.lower():
                companyName = potenName
            print("Body: " + self.FindDomain(userSubmission.selftext.replace("\n", "")))
            #Post Url
            potenName = self.FindDomain(userSubmission.url.replace("\n", ""))
            if companyName == "" and potenName.lower() in postTitle.lower():
                    companyName = potenName
            print("Url: " + self.FindDomain(userSubmission.url.replace("\n", "")))
            #Post Comments
            if companyName == "":
                for comment in userSubmission.comments:
                    if comment.is_submitter == True:
                        potenName = self.FindDomain(comment.body.replace("\n", ""))
                        print("OP Comment: " + comment.body.replace("\n", ""))
                        if potenName.lower() in postTitle.lower():
                            companyName = potenName
                        #print("OP Comment: " + self.FindDomain(userSubmission.url.replace("\n", "")))
            
            print()
            #If company  name still not found. 
            i = i + 1
            print(str(i) + " Title: " + postTitle)
            print("Company Name: " + companyName)
            print("-----------------------------------")
            if companyName != "":
                successPosts.append((companyName, postTitle))
            else:
                failPosts.append((userSubmission, postTitle))
                fail.write(userSubmission.id + "\n")
                fail.write(postTitle + "\n")
            companyName = ""
    
        fail.close()

        print("Correct Results: ")
        for captured in successPosts:
            print(captured)

        print("Correct:" + str(len(successPosts)-1))
        print("Wrong: " + str(len(failPosts)-1))
        #print("Correct: " + str(len(successPosts)/(len(successPosts)+len(failPosts))))
        #print("Fail: " + str(len(failPosts)/(len(successPosts)+len(failPosts))))
        input()
        """
        for captured in failPosts:
            print(captured)
        
        print("Correct: " + str(len(successPosts)/(len(successPosts)+len(failPosts))))
        print("Fail: " + str(len(failPosts)/(len(successPosts)+len(failPosts))))

                #redditList = open("Posts.txt", "r", encoding = 'utf-8')
        """

        """
        #Compare Title with Body
            
        #Conditions
            Capture between wwww. and .com
            If no body compare with url

        #Optimizations
            There is a possibility that there is no url to store. Most likely found in comments by OP

        postTitle = ""
        postBody = ""
        readBody = False 
        successPosts = [()]
        failPosts = [()]
        for x in redditList:
            i = i + 1
            if "Title:" in x:
                postTitle = x
            if "Body:" in x:
                start = x.find("://")
                end = x.find(".com")
                for link in range(start, end):
                    postBody += x[link]
                postBody = postBody.replace("://", "")
                postBody = postBody.replace("www.", "")
            if "Url:" in x:
                if "Daily Chat" in postTitle:
                    postBody = ""
                    continue
                if postBody == "":
                    start = x.find("://")
                    end = x.find(".com")
                    for link in range(start, end):
                        postBody += x[link]
                    postBody = postBody.replace("://", "")
                    postBody = postBody.replace("www.", "")
                
                
                if postBody != "" and str(postBody.lower()) in str(postTitle.lower()):
                    successPosts.append((postTitle, postBody))
                else:
                    failPosts.append((postTitle, postBody))
            postBody = ""
        """
