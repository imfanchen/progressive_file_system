import uuid
from bank_system import BankSystem
from dataclasses import dataclass, field
from enum import Enum


class BankSystemBasicImpl(BankSystem):
    def __init__(self):
        self.accounts = {}  # {account_id: {balance: int, transactions: list[dict]}}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = {"balance": 0, "transactions": []}
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        account["balance"] += amount
        account["transactions"].append(
            {
                "timestamp": timestamp,
                "amount": amount,
            }
        )
        return account["balance"]

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        if account["balance"] < amount:
            return None
        account["balance"] -= amount
        account["transactions"].append(
            {
                "timestamp": timestamp,
                "amount": -amount,
            }
        )
        return account["balance"]

    def top_activity(self, timestamp: int, n: int) -> str:
        activities = []
        for account_id, account in self.accounts.items():
            total_value = sum(
                abs(tx["amount"])
                for tx in account["transactions"]
                if tx["timestamp"] < timestamp
            )
            activities.append((account_id, total_value))

        activities.sort(key=lambda x: (-x[1], x[0]))

        result_parts = []
        for account_id, value in activities[:n]:
            result_parts.append(f"{account_id}({value})")

        return ", ".join(result_parts)


class TransactionStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CANCELLED = "CANCELLED"


@dataclass
class Transaction:
    transaction_id: str
    timestamp: int
    amount: int
    account_id: str
    status: TransactionStatus


@dataclass
class Account:
    account_id: str
    created_at: int
    balance: int = 0
    transactions: dict[str, Transaction] = field(default_factory=dict)
    is_deactivated: bool = False
    deactivated_at: int | None = None

    def can_deposit(self, amount: int = 0) -> bool:
        return not self.is_deactivated and not amount <= 0

    def deposit(self, timestamp: int, amount: int) -> str:
        transaction_id = str(uuid.uuid4())
        if self.can_deposit(amount):
            self.balance += amount
            self.transactions[transaction_id] = Transaction(
                transaction_id,
                timestamp,
                amount,
                self.account_id,
                TransactionStatus.SUCCESS,
            )
        else:
            self.transactions[transaction_id] = Transaction(
                transaction_id,
                timestamp,
                amount,
                self.account_id,
                TransactionStatus.FAILURE,
            )
        return transaction_id

    def can_withdraw(self, amount: int) -> bool:
        return not self.is_deactivated and self.balance >= amount

    def start_withdraw(self, timestamp: int, amount: int) -> str:
        transaction_id = str(uuid.uuid4())
        if self.can_withdraw(amount):
            self.balance -= amount
            self.transactions[transaction_id] = Transaction(
                transaction_id,
                timestamp,
                -amount,
                self.account_id,
                TransactionStatus.PENDING,
            )
        else:
            self.transactions[transaction_id] = Transaction(
                transaction_id,
                timestamp,
                -amount,
                self.account_id,
                TransactionStatus.FAILURE,
            )
        return transaction_id

    def finalize_withdraw(self, transaction_id: str) -> bool:
        if transaction_id not in self.transactions:
            return False
        transaction = self.transactions[transaction_id]
        if transaction.status != TransactionStatus.PENDING:
            return False
        transaction.status = TransactionStatus.SUCCESS
        return True

    def cancel_withdraw(self, transaction_id: str) -> bool:
        if transaction_id not in self.transactions:
            return False
        transaction = self.transactions[transaction_id]
        if transaction.status != TransactionStatus.PENDING:
            return False
        self.balance += abs(transaction.amount)
        transaction.status = TransactionStatus.CANCELLED
        return True

    def deactivate(self, timestamp: int) -> bool:
        if self.is_deactivated:
            return False
        self.is_deactivated = True
        self.deactivated_at = timestamp
        return True


@dataclass
class Transfer:
    transfer_id: str
    source_account_id: str
    source_transaction_id: str
    target_account_id: str
    target_transaction_id: str
    amount: int
    timestamp: int
    time_to_live: int =  24 * 60 * 60 * 1000
    is_accepted: bool = False
    accepted_at: int | None = None

    def is_expired(self, timestamp: int) -> bool:
        return timestamp > self.timestamp + self.time_to_live

    def accept(self, timestamp: int, transaction_id: str) -> bool:
        if self.is_expired(timestamp) or self.is_accepted:
            return False
        self.is_accepted = True
        self.accepted_at = timestamp
        self.target_transaction_id = transaction_id
        return True


class BankSystemAdvancedImpl(BankSystem):
    def __init__(self):
        self.accounts: dict[str, Account] = {}
        self.transfers: dict[str, Transfer] = {}
        self.transfer_counter = 0

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id, timestamp)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        if not account.can_deposit(amount):
            return None
        account.deposit(timestamp, amount)
        return account.balance

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        if not account.can_withdraw(amount):
            return None
        transaction_id = account.start_withdraw(timestamp, amount)
        account.finalize_withdraw(transaction_id)
        return account.balance

    def top_activity(self, timestamp: int, n: int) -> str:
        activities = [
            (
                account_id,
                sum(
                    abs(tx.amount)
                    for tx in account.transactions
                    if tx.timestamp < timestamp
                    and tx.status == TransactionStatus.SUCCESS
                ),
            )
            for account_id, account in self.accounts.items()
        ]
        activities.sort(key=lambda x: (-x[1], x[0]))
        return ", ".join(f"{acc}({val})" for acc, val in activities[:n])

    def transfer(
        self,
        timestamp: int,
        source_account_id: str,
        target_account_id: str,
        amount: int,
    ) -> str:
        if (
            source_account_id == target_account_id
            or source_account_id not in self.accounts
            or target_account_id not in self.accounts
        ):
            return ""
        source_account = self.accounts[source_account_id]
        if not source_account.can_withdraw(amount):
            return ""
        source_transaction_id = source_account.start_withdraw(timestamp, amount)
        self.transfer_counter += 1
        transfer_id = f"transfer{self.transfer_counter}"
        self.transfers[transfer_id] = Transfer(
            transfer_id,
            source_account_id,
            source_transaction_id,
            target_account_id,
            "",
            amount,
            timestamp,
        )
        return transfer_id

    def accept_transfer(
        self, timestamp: int, account_id: str, transfer_id: str
    ) -> bool:
        if transfer_id not in self.transfers:
            return False
        transfer = self.transfers[transfer_id]
        if transfer.is_accepted or transfer.target_account_id != account_id:
            return False
        source_account = self.accounts[transfer.source_account_id]
        target_account = self.accounts[transfer.target_account_id]
        if (
            transfer.is_expired(timestamp)
            or not source_account.can_withdraw(transfer.amount)
            or not target_account.can_deposit(transfer.amount)
        ):
            source_account.cancel_withdraw(transfer.source_transaction_id)
            return False

        source_account.finalize_withdraw(transfer.source_transaction_id)
        target_transaction_id = target_account.deposit(timestamp, transfer.amount)
        transfer.accept(timestamp, target_transaction_id)
        return True

    def merge_accounts(
        self, timestamp: int, account_id_1: str, account_id_2: str
    ) -> bool:
        if (
            account_id_1 not in self.accounts
            or account_id_2 not in self.accounts
            or account_id_1 == account_id_2
        ):
            return False
        account_1 = self.accounts[account_id_1]
        account_2 = self.accounts[account_id_2]
        if account_1.is_deactivated or account_2.is_deactivated:
            return False
        account_2.balance += account_1.balance
        for transaction in account_1.transactions:
            transaction.account_id = account_id_2
            account_2.transactions.append(transaction)
        account_2.transactions.sort(key=lambda tx: tx.timestamp)
        for transfer in self.transfers.values():
            if not transfer.is_accepted:
                if transfer.source_account_id == account_id_1:
                    transfer.source_account_id = account_id_2
                if transfer.target_account_id == account_id_1:
                    transfer.target_account_id = account_id_2
        account_1.deactivate(timestamp)
        return True

    def get_balance(
        self, timestamp: int, account_id: str, timestamp_at: int
    ) -> int | None:
        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        if account.created_at > timestamp_at:
            return None
        if account.is_deactivated and account.deactivated_at <= timestamp_at:
            return None
        amounts = [
            tx.amount
            for tx in account.transactions
            if tx.timestamp <= timestamp_at
            and tx.timestamp < timestamp
            and (
                tx.status == TransactionStatus.PENDING
                or tx.status == TransactionStatus.SUCCESS
            )
        ]
        return sum(amounts)
