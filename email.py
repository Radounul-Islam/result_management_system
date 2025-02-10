import yagmail
yag = yagmail.SMTP("radoun086@gmail.com", "coap lbzm cskr qirb")
yag.send("inajmul142@gmail.com", "Email using python", "I have sent email using python", attachments="results.csv")
