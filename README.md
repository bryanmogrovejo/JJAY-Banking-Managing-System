# JJAY Banking Managing System

## Team
- Heidi Gonzalez
- Bryan Mogrovejo

## Features
- Creat a bank account with an account id of 5 digits, account name, and starting balance
- Deposit & withdraw
- Transfer funds from one account into another
- Check account balance & view transaction history
- Loads 10,000 accounts with fake data from a csv file to test search and sort algorithms
- Reports sorted by either account id, account name, or account balance
- Three sorting algorithms with built-in timing:
  - Counting Sort 
  - Merge Sort
  - Insertion Sort
- Three searching algorithms with built-in timing:
  - Binary Search
  - Jump Search
  - Linear Search

## Program Language and Library
- Python 3
- Standard library with modules:
  - csv
  - math
  - time
  - deque (from collections)
 
## Instructions to compile/run
After cloning the repo, the user will run the program and be prompted with a main menu. In the menu, a numbered drop down appears with different options. The user can then choose to create however many accounts they would like or, load the csv file with 10k datasets for testing purposes. If the user decides to load in the csv file, any account created manually with get combined with the csv and turn into 1, already sorted.

## Sample
```
JJAY Banking Management System

1.  Create Account
2.  Deposit
...
10. Exit

Enter option: 7
CSV path (default: bank_accounts.csv):

Loaded 10000 accounts.

Sample accounts:
  ID: 10142 | Name: Sarah Hill      | Balance: $216,584.99
  ID: 10086 | Name: David Johnson   | Balance: $57,579.95
  

Enter option: 8
Search by:  1. Binary Search by ID   2. Jump Search by ID   3. Linear Search by Name
Choice: 1
Account ID: 10001
[Binary Search] Found 10142 | Sarah Hill | $216,584.99 (avg 0.0015 ms)

Enter option: 9
Sort algorithm:  1. Counting   2. Merge    3. Insertion
Choice: 1
Sort by:  1. Account ID   2. Name   3. Balance
Choice: 3

--- Account Report (sorted by balance using Counting Sort) ---
Sorted 10000 accounts in 6.20 ms
ID         Name                        Balance
----------------------------------------------
10007      John Carter        $    120,528.02
...
```

## Algorithms 
- Sorting
  - Counting sort
    - This algoritm doesn't compare items, instead it counts how many times a   value appears. It then uses that count to place items into correct positions. It is O(n + k) and only works with integers.
  - Merge Sort
    - This algorithm splits a list in half, then sorts each half, then merges each sorted half to create a sorted list. It is O(n logn)
  - Insertion Sort
    - This algoritm builds a sorted list one item at a time by sorting each element into it's correct spot one by one. It is O(n) with small data but slows down with higher data (like we have) to O(n²)
 

- Searching
  - Binary Search
    - This algorithm cuts the search range in half, checks the middle element, then goes either left or right based on where the target is closer. It is O(logn) and needs to have a sorted list to work with.
  - Jump Search
    - This algorithm jumps ahead through the sorted list in fixed steps of √n until it goes over the target, then falls back to the actual target. It is O(√n) and can be faster than binary search given the location of the item.
  - Linear Search
    - This algorithm walks through every account one by one until it finds a match at O(n). Since names aren't sorted, we can use this algorithm to search by name.
