from abc import ABC

class BankSystem(ABC):
    """
    BankSystem interface for a simplified banking system supporting multiple levels of operations.
    """

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Create a new account with the given account_id if it doesn't already exist.
        Returns True if the account was successfully created or False if an account with account_id already exists.
        """
        pass

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Deposit the given amount of money to the specified account account_id.
        Returns the total amount of money in the account (balance) after processing the query.
        If the specified account does not exist, should return None.
        """
        pass

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Withdraw the given amount of money from the specified account.
        Returns the amount of money in the account (balance) after processing the query.
        If the specified account does not exist, or if the account has insufficient funds, should return None.
        """
        pass

    def top_activity(self, timestamp: int, n: int) -> str:
        """
        Return the top n accounts with the highest total value of transactions sorted in descending order.
        Format: <account_id>(<transactionValue>), ...
        If less than n accounts exist, return all active accounts in the described format.
        """
        pass

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> str:
        """
        Initiate a transfer between accounts. Withdraw amount from source and hold until accepted or expired.
        Returns a unique transfer ID if successful, or empty string if invalid.
        """
        pass

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        """
        Accept the transfer with the given transfer_id.
        Returns True if the transfer was successfully accepted or False otherwise.
        """
        pass

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        """
        Merge two accounts while retaining both accounts' balance, transactions, and transfers.
        Returns True if merge was successful, False otherwise.
        """
        pass

    def get_balance(self, timestamp: int, account_id: str, timestamp_at: int) -> int | None:
        """
        Get the balance of the account at the given timestamp.
        Returns the balance of the account at the given timestamp.
        If the account does not exist, or is deactivated at the given timestamp, returns None.
        """
        pass