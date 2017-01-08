def createHTML(start,end):

	#listNum = [random.randrange(1,104) for i in range(0,40)] # NNP GZC CAR '10WHITE'
	count = 0
	listNum = []
	while count < 20:
		num = random.randrange(start,end)
		
		if num in listNum: continue
		listNum.append(num)
		print(listNum)
		count += 1

	l = ["http://pachy.cs.uic.edu:5000/api/image/src/"+str(i)+"/?resize_pix_w=500" for i in listNum[0:20]]

	index = 0
	for i in range(0,20):
		print("   <td>")
		print("      <center><br><input type='radio' value='share' name='"+ str(listNum[i])+"' id='" + str(listNum[i]) + ",share'>Share")
		print("      <input type='radio' value='do not share' name='"+ str(listNum[i])+"' id='" + str(listNum[i]) + ",do_not_share'>Do not share</center>")
		print('      <img src = "' + l[index] + '" alt="Unavailable"/>')
		print('   </td>')
		if (i+1)%2 == 0:
			print('</tr>')
			print('<tr>')
		index += 1

createHTML(1,104) ## NNP GZC CAR '10WHITE' PERSON 'A'

createHTML(467,644) ## NNP GZC CAR '13WHITE' PERSON 'B'

createHTML(803,929) ## NNP GZC CAR '15WHITE' PERSON 'A'

createHTML(1475,1723) ## NNP GZC CAR '1PURPLE' PERSON 'B'

createHTML(3064,3168) ## NNP GZC CAR '1WHITE' PERSON 'A'