class Post:
    def __init__(self, postIdx, title, location, detailAddress, pay, commentCnt):
        self.postIdx = postIdx
        self.title = title
        self.location = location
        self.detailAddress = detailAddress
        self.pay = pay
        self.commentCnt = commentCnt
    
    def Modify(title, content, location, pay):
        self.title = title
        self.content = content
        self.location = location
        self.pay = pay

    def Delete():
        

    def getLocation():
        return self.location

    def getPay():
        return self.pay

    def getTitle():
        return self.title

    def getCommentCnt():
        return self.commentCnt

