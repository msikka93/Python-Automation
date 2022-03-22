#check if a number is a palindrome or not
import string
class Test:
    def isPalindromeNumber(self):
        num=int(input("Enter a number:"))
        temp=num
        rev=0
        while(num>0):
            dig=num%10
            rev=rev*10+dig
            num=num//10
        if(temp==rev):
            print("The number is a palindrome!")
        else:
            print("Not a palindrome!")

    #check if a string is palindrome or not
    def isPalindromeString(self):
        s=input("Enter a string:")
        valid = set(string.ascii_letters)
        result_s=''.join([ch for ch in s if ch in valid])
        a = result_s.casefold()
        if(a == a[::-1]):
            print("The string is a palindrome!")
        else:
            print("Not a palindrome")

    def longestpalindromes(self,text):
        text = text.lower()
        results = []

        for i in range(len(text)):
            for j in range(0, i):
                chunk = text[j:i + 1]

                if chunk == chunk[::-1]:
                    results.append(chunk)

        return text.rindex(max(results, key=len)), results

    def longestPalindrome(self,s) -> str:
        # Create a string to store our resultant palindrome
        palindrome = ''
        # loop through the input string
        for i in range(len(s)):
            # loop backwards through the input string
            for j in range(len(s), i, -1):
                # Break if out of range
                if len(palindrome) >= j - i:
                    break
                # Update variable if matches
                elif s[i:j] == s[i:j][::-1]:
                    palindrome = s[i:j]
                    break

        return palindrome

if __name__ == "__main__":
    a = Test()
    #a.isPalindromeNumber()
    #a.isPalindromeString()
    # b=a.longestpalindromes('forgeeksskeegfor')
    # print(b)
    b = a.longestPalindrome('forgeeksskeegfor')
    print(b)