from context import EHRM

#Emulates a truth-machine
#Takes input (0/1)
#If 0, Print 0 and exit
#If 1, Print 1 forever
runner = EHRM("DE9EC", debug=False)

runner.run()