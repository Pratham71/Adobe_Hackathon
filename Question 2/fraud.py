def fraud(time_30_mins, transactions):
    fraud_transaction = []
    for i in transactions:
        if i[0] in time_30_mins:
            fraud_transaction.append(i[1:])

    # Print
    return fraud_transaction
