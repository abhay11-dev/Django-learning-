import logging

logger = logging.getLogger(__name__)

def send_failure_alert(txn, error):
    message = f"""
        🚨 CRITICAL TRANSACTION FAILURE 🚨
        Transaction ID: {txn.id}
        Sender: {txn.sender_id}
        Receiver: {txn.receiver_id}
        Amount: {txn.amount}
        Error: {error}
        Status: {txn.status}
    """

    logger.critical(message)
    print(message)