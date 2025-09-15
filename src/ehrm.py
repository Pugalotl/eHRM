class EHRM:
	def __init__(self, script, ram_len=100):
		#Defines the code, RAM, memory and pointer
		self.script = script
		self.ram = [0] * ram_len
		self.ram_len = ram_len
		self.mem = 0
		self.INSTRUCTION_LENGTH = 4
		
	def get_mem(self, pointer):
		#If the pointer is -1, return memory, else return the RAM at the pointer
		if (pointer == -1):
			return self.mem
		else:
			if (pointer < 0 and pointer > self.ram_len):
				raise Exception("Pointer out of range.")
				return -1
			
			return self.ram[pointer]
			
	def set_mem(self, pointer, val):
		#If the pointer is -1, set memory, else set the RAM at the pointer
		val = val % self.INSTRUCTION_LENGTH
		if (pointer == -1):
			self.mem = val
		else:
			if (pointer < 0 and pointer > self.ram_len):
				raise Exception("Pointer out of range.")
			
			self.ram[pointer] = val
			
	def run(self):
		#Runs the program
		#Each instruction's value is given below:
		#		0				1				2				3
		#		...				ADD 1			ADD 2			ADD 3
		#		4				5				6				7
		#		SEL 0			SEL -1			SEL +1			SEL RAM/MEM
		#		8				9				A				B
		#		WHILE 0			WHILE 1			WHILE 2			WHILE 3
		#		C				D				E				F
		#		ENDWHILE		INPUT			OUTPUT			...
		
		code_pointer = 0
		mem_pointer = 0
		prev_mem_pointer = -1
		input_mode = "2B"
		
		while (code_pointer < len(self.script)):
			instruction = self.script[code_pointer]
			
			if (instruction in "123"):
				#ADD 1,2,3
				#Converts the instruction into an int to add to the current memory
				val = self.get_mem( mem_pointer ) + int(instruction)
				self.set_mem(mem_pointer, val)
				
			if (instruction == "4"):
				#SEL 0
				mem_pointer = 0
				
			if (instruction == "5"):
				#SEL -1
				#Makes sure memory does not wrap around
				mem_pointer = max(0, mem_pointer - 1)
				
			if (instruction == "6"):
				#SEL +1
				#Makes sure memory does not wrap around
				mem_pointer = min(mem_pointer + 1, self.ram_len-1)
				
			if (instruction == "7"):
				#SEL MEM / RAM
				#Swaps between the RAM and the memory cell
				#Uses the two variables to achieve the swap
				mem_pointer, prev_mem_pointer = prev_mem_pointer, mem_pointer
				
			#...
			
			if (instruction == "D"):
				#INPUT
				#Checks which mode I/O is in and does input accordingly
				if (input_mode == "2B"):
					#2 Bit Input
					input_val = int(input("> ")) % self.INSTRUCTION_LENGTH
					self.set_mem(mem_pointer, input_val)
					
			if (instruction == "E"):
				#OUTPUT
				#Checks which mode I/O is in and does output accordingly
				if (input_mode == "2B"):
					#2 Bit Output
					output_val = self.get_mem(mem_pointer)
					print(output_val, end="")
				
			if (instruction == "?"):
				#Debugs program by printing the memory and RAM (first 10 values)
				self.pprint()
			
			code_pointer += 1
			
	def pprint(self):
		print(f"MEM: [{self.mem}]\nRAM: {self.ram[:10]}")