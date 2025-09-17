class EHRM:
	def __init__(self, script, ram_len=100):
		#Defines the code, RAM, memory and pointer
		self.script = script.replace(" ","")
		self.ram = [0] * ram_len
		self.ram_len = ram_len
		self.mem = 0
		self.INSTRUCTION_LENGTH = 4
		self.base_printable = self.gen_chars(script)
		
	def gen_chars(self, script):
		#Generates the 4 printable characters
		#Will be 0,1,2,3 unless there are characters after a F instruction
		base_printable = "0123"
		f_position = script.find("F")
		if (f_position != -1):
			chars = bytes.fromhex(script[f_position+1:]).decode("utf-8")
			base_printable = (chars + base_printable[ - ( 4 - len(chars) ) : ])[:4]

		return base_printable
		
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
		#Each instruction's name is given below:
		#		0				1				2				3
		#		I/O MODE		ADD 1			ADD 2			ADD 3
		#		4				5				6				7
		#		SEL 0			SEL -1			SEL +1			SEL RAM/MEM
		#		8				9				A				B
		#		WHILE 0			WHILE !0		...				...
		#		C				D				E				F
		#		ENDWHILE		INPUT			OUTPUT			END PROGRAM
		
		code_pointer = 0
		mem_pointer = 0
		prev_mem_pointer = -1
		input_mode = "2B"
		while_stack = []
		chars = []
		chars_output = []
		
		while (code_pointer < len(self.script)):
			instruction = self.script[code_pointer]
			
			if (instruction == "0"):
				#I/O MODE
				#Switches between ASCII and 2B
				input_mode = "ASCII" if input_mode == "2B" else "2B"
			
			elif (instruction in "123"):
				#ADD 1,2,3
				#Converts the instruction into an int to add to the current memory
				val = self.get_mem( mem_pointer ) + int(instruction, 16)
				self.set_mem(mem_pointer, val)
				
			elif (instruction == "4"):
				#SEL 0
				mem_pointer = 0
				
			elif (instruction == "5"):
				#SEL -1
				#Makes sure memory does not wrap around
				mem_pointer = max(0, mem_pointer - 1)
				
			elif (instruction == "6"):
				#SEL +1
				#Makes sure memory does not wrap around
				mem_pointer = min(mem_pointer + 1, self.ram_len-1)
				
			elif (instruction == "7"):
				#SEL MEM / RAM
				#Swaps between the RAM and the memory cell
				#Uses the two variables to achieve the swap
				mem_pointer, prev_mem_pointer = prev_mem_pointer, mem_pointer
				
			elif (instruction in "89"):
				#WHILE 0,!0
				cur_val = self.get_mem( mem_pointer )
				
				if (instruction == "8" and cur_val != 0) or (instruction == "9" and cur_val == 0):
					#Finds the ENDWHILE block if the two values are not equal
					while (self.script[code_pointer] != "C"):
						code_pointer += 1
				else:
					#Adds the starting position and value to check to the stack
					while_stack.append( [code_pointer, instruction] )
					
			elif (instruction == "C"):
				#ENDWHILE
				#Jumps back to start if memory value is equal to while_value
				cur_val = self.get_mem( mem_pointer )
				
				if (while_stack[-1][1] == "8" and cur_val == 0) or (while_stack[-1][1] == "9" and cur_val != 0):
					#If current value is equal to while value, jump back to code pointer
					code_pointer = while_stack[-1][0]
				else:
					while_stack.pop()
			
			elif (instruction == "D"):
				#INPUT
				#Checks which mode I/O is in and does input accordingly
				if (input_mode == "2B"):
					#2 Bit Input
					input_val = self.base_printable.index(input("")[0])
					self.set_mem( mem_pointer, input_val )
				elif (input_mode == "ASCII"):
					if (len(chars) == 0):
						input_char_num = ord(input()[0])
						chars = [input_char_num>>(x*2)&3 for x in range(4)]
						self.set_mem( mem_pointer, chars.pop() )
					else:
						self.set_mem( mem_pointer, chars.pop() )
					
			elif (instruction == "E"):
				#OUTPUT
				#Checks which mode I/O is in and does output accordingly
				if (input_mode == "2B"):
					#2 Bit Output
					output_val = self.get_mem( mem_pointer )
					print(self.base_printable[output_val], end="")
				elif (input_mode == "ASCII"):
					chars_output.append( self.get_mem( mem_pointer ) )
					if (len(chars_output) >= 4):
						base_num = 0
						for num in chars_output:
							base_num = base_num << 2
							base_num += num
						print(chr(base_num), end="")
						chars_output = []
					
			elif (instruction == "F"):
				#END PROGRAM
				break
				
			elif (instruction == "?"):
				#Debugs program by printing the memory and RAM (first 10 values)
				self.pprint()
			
			code_pointer += 1
			
		print()
			
	def pprint(self):
		print(f"MEM: [{self.mem}]\nRAM: {self.ram[:10]}")