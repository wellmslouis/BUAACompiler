import sys

procedure=""
for l in sys.stdin:
    procedure+=l
a=""
for i in range(len(procedure)):
    if procedure[i]=="\n" or procedure[i]=="\r":
        a+="[]"
    else:
        a+=procedure[i]
print(a)