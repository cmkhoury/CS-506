'''
This file is for the helper functions.
CalculateCost
GetLocation
EncodeLocation
GetRecommendedPartners
and so on...
'''

import bcrypt

#calculate the total cost of one order/cart
def CalculateCost(base, add):
        return base+add

#calculate how much still needed for free shipping
def CalculateLeft(line, cost):
        return line-cost

#check whether the current cost reach the free shipping line
def ReachLine(line, cost):
    if(CalculateLeft(line, cost)<0):
        return True
    return False

#encrypt the user's password for security purpose
def encryptPassword(password):
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

#check and match the password
def checkPassword(inputPWD, hashedPWD):
    return bcrypt.checkpw(inputPWD, hashedPWD)
