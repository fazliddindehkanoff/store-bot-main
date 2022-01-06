def formatPhoneNumber(phone):
    phone = str(phone)
    if len(phone) == 12:
        return f"({phone[3:5]}){phone[5:8]}-{phone[8:10]}-{phone[10:12]}"

    elif len(phone) == 13:
        return f"({phone[4:6]}){phone[6:9]}-{phone[9:11]}-{phone[11:13]}"
