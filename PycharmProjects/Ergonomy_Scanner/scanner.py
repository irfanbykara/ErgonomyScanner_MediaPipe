
class Distance:
    def get_x_distance(self, pos1,pos2 ):
        return (abs(pos1[1]) - abs(pos2[1]))
    def get_y_distance(self, pos1, pos2):
        return abs(pos1[2]) - abs(pos2[2])
    def get_euclidian_distance(self,pos1,pos2):
        return ((pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)**0.5


class ScanErgonomy():
    def __init__(self, lmlist):
        self.lmlist = lmlist
        self.dist = Distance()

    def ergonomy_checker(self):
        shoulder_mean_x = self.dist.get_x_distance(self.lmlist[12],self.lmlist[11])/2
        shoulder_mean_y = abs((self.lmlist[12][2]+self.lmlist[11][2])/2)
        hib_mean_x = self.dist.get_x_distance(self.lmlist[24],self.lmlist[23])/2
        hib_mean_y = abs((self.lmlist[24][2]+self.lmlist[23][2])/2)
        knee_mean_x = self.dist.get_x_distance(self.lmlist[26],self.lmlist[25])/2
        knee_mean_y = self.dist.get_y_distance(self.lmlist[26],self.lmlist[25])/2
        belly_button_x = (self.lmlist[24][1]+self.lmlist[23][1])/2
        belly_button_y = (shoulder_mean_y - hib_mean_y)/3+hib_mean_y

        # If hands are above eyes...
        if self.dist.get_y_distance(self.lmlist[15], self.lmlist[4]) <= 0 or self.dist.get_y_distance(self.lmlist[16], self.lmlist[4]) <= 0 :
            print('your hands are above eyes... ')
            return False

        # # If hands are so close to the cross-shoulders
        if abs(self.dist.get_euclidian_distance(self.lmlist[15],self.lmlist[12]))<=50 or abs(self.dist.get_euclidian_distance(self.lmlist[16],self.lmlist[11]))<=50:
            print('your hands are so close to the cross shoulders. ')

            return False
        # #If hands are so close to the knee
        if abs(self.dist.get_y_distance(self.lmlist[15],self.lmlist[26]))<=50 or abs(self.dist.get_y_distance(self.lmlist[16],self.lmlist[25]))<=50:
            print('Your hands are so close to the knees ')
            return False

        #If you are squatting too much.
        if abs(self.dist.get_y_distance(self.lmlist[24],self.lmlist[30])) <= 175 or abs(self.dist.get_euclidian_distance(self.lmlist[23],self.lmlist[29])) <= 175:
            print('You are  squatting too much...')
            return False
        # If you are bending too much...
        if abs(hib_mean_y-shoulder_mean_y) <= 100 :
            print('Bending too much.')

            return False
        return True





