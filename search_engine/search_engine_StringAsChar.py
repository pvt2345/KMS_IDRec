import os

path =os.path.dirname(__file__)
path_char = os.path.join(path,'Character.txt')
class search_engine_StringAsChar:
    def __init__(self, pattern):
        self.Pattern = pattern
        with open(path_char, 'r') as f:
            self.Character = f.read().splitlines()
        f.close()
        # print(self.Character)
        self.P = list(set(self.Pattern.split()))
        # print(self.P)

        self.EncodedPattern = []
        for item in self.Pattern.split():
            for i in range(len(self.P)):
                if(item == self.P[i]):
                    self.EncodedPattern.append(self.Character[i])

        self.EncodedPattern = ''.join(self.EncodedPattern)
        # print(self.EncodedPattern)

    def Encoding(self, S):
        self.EncodedString = []
        for item in S.lower().split():
            for i in range(len(self.P)):
                if(item == self.P[i]):
                    self.EncodedString.append(self.Character[i])
                    break
                if(i == len(self.P) - 1):
                    self.EncodedString.append('#')

        self.EncodedString = ''.join(self.EncodedString)


    #hàm so 2 xâu đc mã hóa
    def doXapXi(self, S, P):
        M = 0
        for t in range(0, len(P)):
            M += (len(P) - t)*(t+1)

        #M ok
        # print(M)
        H = 0
        for t in range(1, len(P) + 1):
            for i in range(0, len(P) - t + 1):
                if(S.find(P[i:i+t]) >= 0): #tìm được khúc con của P trong S
                    H = H + t

        # print(H)
        F = H/M

        return F

    def Search(self, string):
        self.Encoding(string)
        a = self.doXapXi(self.EncodedString, self.EncodedPattern)
        #lấy vị trí
        # index_ = []
        #
        # for index, c in enumerate(self.EncodedString):
        #     if(c != '#'):
        #         index_.append(index)
        #
        # print(index_)
        # position_ = []
        #
        # for index in index_:
        #     position = 0
        #     for i, word in enumerate(string.split()):
        #         position += (1 + len(word))
        #         if i >= index:
        #             start = position - len(word) - 1
        #             position_.append((start, position))
        #             break

        return a

if __name__ == '__main__':
    # print(doXapXi('abaadfsdfsdc', 'abdfsdf'))

    a = search_engine_StringAsChar('thuế xuất thực phẩm nhập khẩu , ')

    # print(a.EncodedPattern)
    string = 'Phí thẩm định cấp giấy chứng nhận đối với thực phẩm xuất khẩu theo yêu cầu của nước nhập khẩu'
    # a.Encoding(string)
    # print(len(string.split()))
    print(a.Search(string))
    # print(string[52:5])