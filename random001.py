str = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
str1 = ""
for singchar in str:
    if singchar == 'y':
        newchar = 'a'
    elif singchar == 'z':
        newchar = 'b'
    elif singchar == ' ' or singchar == '.' or singchar == '(' or singchar == ')':
        newchar = singchar
    else:
        newchar = chr(ord(singchar)+2)
    str1 = str1 + newchar

print(str1)
