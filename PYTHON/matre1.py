# Maths Research - Matre 
#Explanation: This program takes an integer input from the user and checks if it is a perfect square.
#If it is not, it multiplies the number by 2 and checks again.
#This process continues until a perfect square is found.
#The program uses the isqrt() function from the math module to find the integer square root of a number. 
import math
def find_perfect_square(num):
    while True:
        sqrt_num = math.isqrt(num)  # Find the integer square root
        if sqrt_num * sqrt_num == num:
            print(f"{num} is a perfect square of {sqrt_num}.")
            break
        else:
            print(f"{num} is not a perfect square, multiplying by 2...")
            num *= 2

# Take input from the user
while True: 
  try:
    num = int(input("Enter a number: "))
    find_perfect_square(num)
  except:
    print("Invalid Syntax. Try again!")