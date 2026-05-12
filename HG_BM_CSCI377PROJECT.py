from collections import deque
import csv
import math
import time


#ACCOUNT CLASS - stores info for each bank account
class Account:
    def __init__(self, account_id, name, balance=0):
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.transactions = deque()  # deque used for the transaction history

    def log(self, msg):
        self.transactions.append(msg)


class BankingSystem:
    def __init__(self):
        self.accounts = {}     # dictionary that maps account ID to account object
        self.sorted_ids = []    # list of IDs kept in sorted order for searching algorithms


                            #Sorting algorithms
                            
    # MERGE SORT - splits the list in half and merges it back together
    def merge_sort(self, arr, key):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], key)
        right = self.merge_sort(arr[mid:], key)
        return self.merge(left, right, key)

    def merge(self, left, right, key):
        result = []
        i = 0
        j = 0
        # compare items from left and right and then picks the smaller one
        while i < len(left) and j < len(right):
            if getattr(left[i], key) <= getattr(right[j], key):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        #adds anything left over from either side
        while i < len(left):
            result.append(left[i])
            i += 1
        while j < len(right):
            result.append(right[j])
            j += 1
        return result

    # INSERTION SORT - builds up the sorted list one item at a time by sliding items into the right spot
    def insertion_sort(self, arr, key):
        arr = arr[:]  # copies the original list so we don't change it
        for i in range(1, len(arr)):
            current = arr[i]
            j = i - 1
            # slides bigger items to the right
            while j >= 0 and getattr(arr[j], key) > getattr(current, key):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = current
        return arr

    # COUNTING SORT works on numbers only, no comparisons needed, just counting
    def counting_sort(self, arr, key):
        if len(arr) == 0:
            return arr

        #pulls out the numeric values we want to sort by
        if key == "balance":
            keys = []
            for a in arr:
                keys.append(int(a.balance))
        elif key == "account_id":
            keys = []
            for a in arr:
                keys.append(int(a.account_id))
        else:
            #since we can't count sort text, we use merge sort instead
            print("Counting sort only works on numbers, using merge sort instead.")
            return self.merge_sort(arr, key)

        min_k = min(keys)
        max_k = max(keys)
        count = [0] * (max_k - min_k + 1)

        #counts how many times each value shows up
        for k in keys:
            count[k - min_k] += 1

        #turns the counts into running totals so we know where to place each one
        for i in range(1, len(count)):
            count[i] += count[i - 1]

        #places each account into the right spot in the result
        result = [None] * len(arr)
        for i in range(len(arr) - 1, -1, -1):
            pos = keys[i] - min_k
            count[pos] -= 1
            result[count[pos]] = arr[i]
        return result


                            #Searching algorithms 
                            
    # BINARY SEARCH - cuts the list in half at each step - only works on sorted lists
    def binary_search(self, account_id):
        low = 0
        high = len(self.sorted_ids) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.sorted_ids[mid] == account_id:
                return mid
            elif self.sorted_ids[mid] < account_id:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    # JUMP SEARCH - jumps ahead in blocks of sqrt(n), then scans inside that block
    def jump_search(self, account_id):
        n = len(self.sorted_ids)
        if n == 0:
            return -1
        step = int(math.sqrt(n))
        prev = 0
        #jump forward until we pass where the ID could be
        while prev < n and self.sorted_ids[min(step, n) - 1] < account_id:
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                return -1
        #check one by one inside the block
        while prev < min(step, n):
            if self.sorted_ids[prev] == account_id:
                return prev
            prev += 1
        return -1

    #LINEAR SEARCH - this just checks each account one by one for a name match
    def linear_search_by_name(self, name):
        results = []
        for a in self.accounts.values():
            if name.lower() in a.name.lower():
                results.append(a)
        return results
    

                    #BANKING OPS

    def create_account(self, account_id, name, balance=0):
        if account_id in self.accounts:
            print("Account ID already exists.")
            return
        acc = Account(account_id, name, balance)
        acc.log(f"Account opened with ${balance:.2f}")
        self.accounts[account_id] = acc
        self.sorted_ids.append(account_id)
        self.sorted_ids.sort()
        print(f"Created account {account_id} ({name}) with ${balance:.2f}")

    def deposit(self, account_id, amount):
        acc = self.accounts.get(account_id)
        if not acc or amount <= 0:
            print("Invalid account/amount.")
            return
        acc.balance += amount
        acc.log(f"Deposit +${amount:.2f} | Balance ${acc.balance:.2f}")
        print(f"Deposited ${amount:.2f}. New balance: ${acc.balance:.2f}")

    def withdraw(self, account_id, amount):
        acc = self.accounts.get(account_id)
        if not acc or amount <= 0:
            print("Invalid account/amount.")
            return
        #checks if they even have enough money first "greedy validation"
        if amount > acc.balance:
            print(f"Not enough funds. Balance: ${acc.balance:.2f}")
            return
        acc.balance -= amount
        acc.log(f"Withdraw -${amount:.2f} | Balance ${acc.balance:.2f}")
        print(f"Withdrew ${amount:.2f}. New balance: ${acc.balance:.2f}")

    def transfer(self, from_id, to_id, amount):
        a = self.accounts.get(from_id)
        b = self.accounts.get(to_id)
        if not a or not b or amount <= 0:
            print("Invalid account/amount.")
            return
        if amount > a.balance:
            print(f"Not enough funds. Balance: ${a.balance:.2f}")
            return
        a.balance -= amount
        b.balance += amount
        a.log(f"Transfer to {to_id}: -${amount:.2f} | Balance ${a.balance:.2f}")
        b.log(f"Transfer from {from_id}: +${amount:.2f} | Balance ${b.balance:.2f}")
        print(f"Transferred ${amount:.2f} from {from_id} to {to_id}.")

    def check_balance(self, account_id):
        acc = self.accounts.get(account_id)
        if not acc:
            print("Account not found.")
            return
        print(f"{account_id} ({acc.name}) | Balance: ${acc.balance:.2f}")

    def view_transactions(self, account_id):
        acc = self.accounts.get(account_id)
        if not acc:
            print("Account not found.")
            return
        print(f"\nTransactions for {acc.name} ({account_id}):")
        if len(acc.transactions) == 0:
            print("  (none)")
        else:
            i = 1
            for t in acc.transactions:
                print(f"  {i}. {t}")
                i += 1

                     #SEARCH AND REPORT FUNCTIONS

    def search_account(self, account_id, algorithm="binary"):
        #runs the search multiple times to get a better average since one run is too fast to measure accurately
        runs = 1000
        if algorithm == "binary":
            search_fn = self.binary_search
            label = "Binary Search"
        else:
            search_fn = self.jump_search
            label = "Jump Search"

        start = time.perf_counter()
        for _ in range(runs):
            idx = search_fn(account_id)
        avg_ms = (time.perf_counter() - start) * 1000 / runs

        if idx == -1:
            print(f"[{label}] Account not found. (avg {avg_ms:.4f} ms)")
            return
        a = self.accounts[account_id]
        print(f"[{label}] Found {account_id} | {a.name} | ${a.balance:.2f} "
              f"(avg {avg_ms:.4f} ms)")

    def search_by_name(self, name):
        #linear search is slow enough to run 100 times
        runs = 100
        start = time.perf_counter()
        for _ in range(runs):
            results = self.linear_search_by_name(name)
        avg_ms = (time.perf_counter() - start) * 1000 / runs

        if len(results) == 0:
            print(f"[Linear Search] No accounts match '{name}'. (avg {avg_ms:.4f} ms)")
            return
        print(f"\n[Linear Search] Matches for '{name}' (avg {avg_ms:.4f} ms):")
        #ONLY print the first 10 matches so it doesn't fill up the screen
        count = 0
        for a in results:
            if count >= 10:
                break
            print(f"  {a.account_id} | {a.name} | ${a.balance:.2f}")
            count += 1
        if len(results) > 10:
            print(f"  ... ({len(results) - 10} more not shown)")

    def generate_report(self, sort_by="account_id", algorithm="merge"):
        if len(self.accounts) == 0:
            print("No accounts to display.")
            return
        all_accounts = list(self.accounts.values())

        start = time.perf_counter()
        if algorithm == "merge":
            sorted_accs = self.merge_sort(all_accounts, sort_by)
            label = "Merge Sort"
        elif algorithm == "insertion":
            sorted_accs = self.insertion_sort(all_accounts, sort_by)
            label = "Insertion Sort"
        else:
            sorted_accs = self.counting_sort(all_accounts, sort_by)
            label = "Counting Sort"
        elapsed_ms = (time.perf_counter() - start) * 1000

        print(f"\n--- Account Report (sorted by {sort_by} using {label}) ---")
        print(f"Sorted {len(sorted_accs)} accounts in {elapsed_ms:.2f} ms")
        print(f"{'ID':<10} {'Name':<22} {'Balance':>12}")
        print("-" * 46)
        #ONLY shows the first 20 rows so the output stays readable
        for i in range(min(20, len(sorted_accs))):
            a = sorted_accs[i]
            print(f"{a.account_id:<10} {a.name:<22} ${a.balance:>11,.2f}")
        if len(sorted_accs) > 20:
            print(f"... ({len(sorted_accs) - 20} more not shown)")

    #CSV loader 

    #Loads accounts from a CSV with columns: account_id, account_name, balance
    def load_from_csv(self, csv_path):
        loaded = 0
        skipped = 0
        new_ids = []
        try:
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    acc_id = row["account_id"].strip()
                    name = row["account_name"].strip()
                    try:
                        balance = float(row["balance"])
                    except ValueError:
                        skipped += 1
                        continue
                    if acc_id in self.accounts:
                        skipped += 1
                        continue
                    acc = Account(acc_id, name, balance)
                    acc.log(f"Account opened with ${balance:.2f}")
                    self.accounts[acc_id] = acc
                    self.sorted_ids.append(acc_id)
                    new_ids.append(acc_id)
                    loaded += 1
        except FileNotFoundError:
            print(f"File not found: {csv_path}")
            return

        #sorts once at the end instead of after every insert for better performance
        self.sorted_ids.sort()
        print(f"\nLoaded {loaded} accounts.")
        if skipped > 0:
            print(f"Skipped {skipped} rows.")

        #showcases a few sample IDs for demo purposes
        if len(new_ids) > 0:
            new_ids.sort()
            picks = [0, len(new_ids) // 4, len(new_ids) // 2,
                     3 * len(new_ids) // 4, len(new_ids) - 1]
            print("\nSample accounts:")
            for i in picks:
                a = self.accounts[new_ids[i]]
                print(f"  ID: {new_ids[i]} | Name: {a.name:<22} | Balance: ${a.balance:,.2f}")


                                #MAIN MENU

def main():
    bank = BankingSystem()

    while True:
        print("\n JJAY Banking Management System\n")
        print("1.  Create Account")
        print("2.  Deposit")
        print("3.  Withdraw")
        print("4.  Transfer")
        print("5.  Check Your Balance")
        print("6.  View Your Transaction History")
        print("7.  Load Accounts from CSV")
        print("8.  Searching")
        print("9.  Sorting")
        print("10. Exit")
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            acc_id = input("Account ID (5 digits): ").strip()
            if not (acc_id.isdigit() and len(acc_id) == 5):
                print("Account ID must be exactly 5 digits.")
                continue
            name = input("Name: ").strip()
            try:
                balance = float(input("Initial balance: "))
            except ValueError:
                print("Invalid number.")
                continue
            bank.create_account(acc_id, name, balance)

        elif choice == "2":
            acc_id = input("Account ID: ").strip()
            try:
                amount = float(input("Deposit amount: "))
            except ValueError:
                print("Invalid number.")
                continue
            bank.deposit(acc_id, amount)

        elif choice == "3":
            acc_id = input("Account ID: ").strip()
            try:
                amount = float(input("Withdrawal amount: "))
            except ValueError:
                print("Invalid number.")
                continue
            bank.withdraw(acc_id, amount)

        elif choice == "4":
            from_id = input("From account ID: ").strip()
            to_id = input("To account ID: ").strip()
            try:
                amount = float(input("Transfer amount: "))
            except ValueError:
                print("Invalid number.")
                continue
            bank.transfer(from_id, to_id, amount)

        elif choice == "5":
            bank.check_balance(input("Account ID: ").strip())

        elif choice == "6":
            bank.view_transactions(input("Account ID: ").strip())

        elif choice == "7":
            path = input("CSV path (default: bank_accounts.csv): ").strip()
            if path == "":
                path = "bank_accounts.csv"
            bank.load_from_csv(path)

        elif choice == "8":
            print("Search by:  1. Binary by ID   2. Jump Search by ID   3. Linear Search by Name")
            s = input("Choice: ").strip()
            if s == "1":
                bank.search_account(input("Account ID: ").strip(), "binary")
            elif s == "2":
                bank.search_account(input("Account ID: ").strip(), "jump")
            elif s == "3":
                bank.search_by_name(input("Name: ").strip())
            else:
                print("Invalid search option.")

        elif choice == "9":
            print("Sort algorithm:  1. Counting   2. Merge    3. Insertion")
            algo_choice = input("Choice: ").strip()
            if algo_choice == "1":
                algo = "counting"
            elif algo_choice == "2":
                algo = "merge"
            elif algo_choice == "3":
                algo = "insertion"
            else:
                print("Invalid sort option.")
                continue
            print("Sort by:  1. Account ID   2. Name   3. Balance")
            field_choice = input("Choice: ").strip()
            if field_choice == "1":
                field = "account_id"
            elif field_choice == "2":
                field = "name"
            elif field_choice == "3":
                field = "balance"
            else:
                print("Invalid field.")
                continue
            bank.generate_report(field, algo)

        elif choice == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
