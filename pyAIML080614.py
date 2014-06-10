import marshal
import aiml
from openWeb import web
import os.path

brain = "std-startup.xml"
learnFile = "standard/learnt.aiml"
k = aiml.Kernel()

def AddToBrain(file, pattern, template):
	fo = open(file, "r")
	line = fo.readlines()
	line = line[:-1]
	a = "<category><pattern>"+pattern.upper()+"</pattern><template>"+template+"</template></category>\n</aiml>"
	line += ''.join(str(e) for e in a)
	fo.close()
	do = open(file, "w")
	do.writelines(line)
	do.close()
	
def LoadBrain():
	if os.path.isfile("standard.brn"):
		k.bootstrap(brainFile = "standard.brn")
		print("brain loaded")
	else:
		k.bootstrap(learnFiles = brain, commands = "load aiml b")
		k.respond("LOAD AIML B")
		k.saveBrain("standard.brn")
		print("new brain created")
	sessionFile = file("javis1.ses", "rb")
	session = marshal.load(sessionFile)
	sessionFile.close()
	for pred,value in session.items():
		k.setPredicate(pred, value, "javis")
	k.setBotPredicate("name","javis")		



LoadBrain()

while True:
	input = raw_input("> ")
	if input == "define":
		a = raw_input("which property would you like to set: ")
		b = raw_input("set to: ")
		k.setBotPredicate(a,b)
		print("updated!")
	elif input == "save brain":
		k.saveBrain("standard.brn")
		print "brain saved !"
	elif input == "reload brain":
		os.remove("standard.brn")
		LoadBrain()
	else:
		response = k.respond(input, "javis")
		
		session = k.getSessionData("javis")
		sessionFile = file("javis1.ses", "wb")
		marshal.dump(session, sessionFile)
		sessionFile.close()
		
		if "!" in response:
			if "eztv" in response:
				print("open web page")
				web("http://eztv.it")
			elif "wiki" in response:
				wiki = response[response.find(",")+1:len(response)]
				print wiki
				web("http://en.wikipedia.org/wiki/"+wiki)
			
		if "@" in response:
			print response
			
			if raw_input("NOT DEFFFINED, would you like to define now: >") == "yes":
				
				pattern = raw_input("create pattern? > ")
				template = raw_input("create template? > ")
				AddToBrain(learnFile, pattern, template)
				k.learn(learnFile)
		else:
			print(response)
		
