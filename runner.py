import os, time

if __name__ == '__main__':
    global pass_word
    print(f"[+]  [{time.strftime('%d-%m-%y %X')}] Automation Create account")
    datas = input(f"[+]  [{time.strftime('%d-%m-%y %X')}] How much account: ")
    list_accountsplit = []
    for i in range(1,int(datas)+1):
        list_accountsplit.append(i)
        
    for i in list_accountsplit:
        os.system("py kick.py")