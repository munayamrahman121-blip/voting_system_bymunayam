ADMIN_PIN="1223"
MIN_AGE = 18

candidates = {} # number -> candidate_name, 0 -> NOTA
voters = {} # roll -> age
ballots = [] # candidate number only, secret
voted = set()

closed = False # the vote hasn't ended yet

while True:
	print("Voting System for OSTAD")
	print("1. Register candidate")
	print("2. Register voter")
	print("3. View candidates")
	print("4. Cast vote")
	print("5. Close election and show results")
	print("q. Exit")

	choice = input("Choose (1-5, 'q' to exit): ").strip().lower()

	if choice == "1":
		if closed or ballots:
			print("Candidate registration is locked")
		else:
			name = input("Candidate name: ").strip().title()
			if not name:
				print("Candidate name can't be empty")
			elif name in candidates.values():
				print("Candidate already registered")
			else:
				candidates[len(candidates)+1] = name
				print(f"{name} registered as candidate #{len(candidates)}")

	if choice == "2":
		if closed or ballots:
			print("Voter registration is locked")
		else:
			roll = input("Roll number: ").strip()
			age = input("Age: ").strip()
			# validation here is skipped
			if int(roll) in voters:
				print("This roll is already registered as a voter")
			else:
				voters[int(roll)] = int(age)
				print("Voter registered")
	if choice == "3":
		print("0. None of the Above (NOTA)")
		for number, name in candidates.items():
			print(f"{number}. {name}")

	if choice == "4":
		if closed:
			print("The election is closed")
		elif not candidates:
			print("No candidate registered yet")
		else:
			roll = input("Your roll number: ").strip()
			if not roll.isdigit() or int(roll) not in voters:
				print("This roll is not registered")
			elif int(roll) in voted:
				print("You've already voted!")
			else:
				print("0. None of the Above (NOTA)")
				for number, name in candidates.items():
					print(f"{number}. {name}")
				while True:
					pick = input("Your choice (number): ").strip()
					if pick.isdigit() and (int(pick) == 0 or int(pick) in candidates):
						break
					print("Invalid choice, try again")
				
				voted.add(int(roll))
				ballots.append(int(pick))
				print("Your vote is recorded")			

	if choice == "5":
		if not candidates or not voters:
			print("Register atleast one candidate and one voter to generate results")
		else:
			if not closed:
				for attempt in range(1, 4):
					if input("Admin PIN: ").strip() == ADMIN_PIN:
						closed = True
						break
					print(f"Wrong PIN, {3 - attempt} attempts")

			if not closed:
				print("Election not closed")
			else:
				counts = {}

				for number in ballots:
					counts[number] = counts.get(number,0) + 1

				rows = []
				for number, name in candidates.items():
					rows.append((counts.get(number,0), name))
				rows.sort(reverse=True) # rank by name, highest to lowest (reversed=True)

				rows.append((counts.get(0, 0), "None of the Above"))
				# rows = [(.., ..), (.., ..), (.., ..)]
				# rows[0][0]

				total = len(ballots)
				print("ELECTION RESULT")
				print(f"{'Candidate':<14}{'Vote':>6}{'%':>8}")
				for votes, name in rows:
					percent = 0
					if total:
						percent = votes/total * 100
					print(f"{name:<14}{votes:>6}{percent:>8}")

				print(f"Turnout: {len(voted)} of {len(voters)}")

				top = rows[0][0] # top candidates vote count
				# top_name = rows[0][1]
				if total == 0:
					print("no votes were casted")
				elif top == 0:
					print("No candidate received any votes")
				else:
					leaders = set()
					for votes, name in rows[:-1]:
						if votes == top:
							leaders.add(name)
					if len(leaders) > 1:
						print(f"Tie between {', '.join(sorted(leaders))} ({top} vote(s) each")
					else:
						print(f"Winner: {leaders.pop()} with {top} vote(s)")				

	elif choice == "q":
		print("Goodbye!")
		break
	else:
		print("Invalid choice, please choose 1-5 or 'q' to exit")