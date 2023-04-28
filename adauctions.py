import sys
import numpy as np

"""
How to run:

python3 adauctions.py [input_filename]

For instance, for the test document, try running
"python3 adauctions.py test"

"""

def load():
	"""
	Loads data from an input file; the name of the input file 
	is passed as a command-line argument.

	Output: 

		data = [w, b, pos, Q]
		n = number of agents
		m = number of ad slots

	"""

	try:
		with open(f"{sys.argv[1]}.txt") as infile:
			data = infile.readlines()
			w = [float(x) for x in data[0].strip('\n').split(',')]
			b = [float(x) for x in data[1].strip('\n').split(',')]
			Q = [float(x) for x in data[2].strip('\n').split(',')]
			pos = [float(x) for x in data[3].strip('\n').split(',')]
			
			n = len(w)
			assert(len(b) == n)
			assert(len(Q) == n)

			m = len(pos)

			return [w, b, pos, Q], n, m
	except:
		sys.exit("Please provide input file as command-line argument")

def print_formatted(x, p):
	# print assignment and price-per-click payments
	for ad_loc, bidder in enumerate(x):
		print(f"Position {ad_loc}: \t bidder {bidder}")

	for bidder, payment in enumerate(p):
		print(f"Bidder {bidder}: \t {payment:.2f}")

def print_bids(bb):
	# print balanced bids
	for bidder, bid in enumerate(bb):
		print(f"Bidder {bidder}: \t {bid:.2f}")

def vcg(w, b, pos, Q):
	num = len(b)
	ad_assignments = []
	payments = []
	for i in range(len(pos)+1):
		payments.append(0)

	extended_pos = pos.copy()
	while len(extended_pos) < num: extended_pos.append(0)

	Qb = (np.multiply(Q, b)).tolist()
	for i in range(num):
		max_bid = max(Qb)
		max_index = Qb.index(max_bid)
		ad_assignments.append(max_index)
		Qb[max_index] = -1

	for k in range(len(pos)):
		agent = ad_assignments[k]
		t = 0
		for j in range(k + 1, num):
			t = t + (extended_pos[ad_assignments[j - 1]] - extended_pos[ad_assignments[j]]) \
				* Q[ad_assignments[j]] \
				* b[ad_assignments[j]]
		payments[agent] = t / (Q[agent] * extended_pos[agent])

	return ad_assignments, payments

def gsp(w, b, pos, Q):
	num = len(b)
	ad_assignments = []
	payments = []
	for i in range(len(pos)+1):
		payments.append(0)

	Qb = (np.multiply(Q, b)).tolist()
	for i in range(num):
		max_bid = max(Qb)
		max_index = Qb.index(max_bid)
		ad_assignments.append(max_index)
		Qb[max_index] = -1

	for k in range(len(pos)):
		agent = ad_assignments[k]
		payments[agent] = Q[ad_assignments[k+1]]*b[ad_assignments[k+1]]/Q[agent]

	return ad_assignments, payments


def balanced_bid(w, pos):
	"""
	IMPORTANT: for only this part (not VCG or GSP), you may assume 
	that all ad qualities are the same.
	"""
	w_copy = w.copy()
	ad_assignments = []
	num = len(w)
	m = len(pos)

	for i in range(num):
		max_bid = max(w_copy)
		max_index = w_copy.index(max_bid)
		ad_assignments.append(max_index)
		w_copy[max_index] = -1

	bids = w.copy()

	for i in range(m-1, 0, -1):
		bi = w[ad_assignments[i]]-((w[ad_assignments[i]]-bids[ad_assignments[i+1]]))\
			 *pos[i]/pos[i-1]
		bids[ad_assignments[i]] = bi
	return bids

def main():
	[w, b, pos, Q], n, m = load()
	vcg_ad_assignments, vcg_payments = vcg(w, b, pos, Q)
	print("VCG:")
	print_formatted(vcg_ad_assignments, vcg_payments)

	gsp_ad_assignments, gsp_payments = gsp(w, b, pos, Q)
	print("\nGSP:")
	print_formatted(gsp_ad_assignments, gsp_payments)
	
	bids = balanced_bid(w, pos)
	print("\nBalanced bids:")
	print_bids(bids)


if __name__ == "__main__":
	main()



"""
TEST OUTPUT: 

w = [10, 4, 2, 1]
b = [10, 4, 2, 1]
Q = [1, 1, 1, 1]
pos = [0.2, 0.18, 0.1]

VCG:

Position 0: 	 bidder 0
Position 1: 	 bidder 1
Position 2: 	 bidder 2
Position 3: 	 bidder 3

Bidder 0: 	 	 1.70
Bidder 1: 	 	 1.44
Bidder 2: 	 	 1.00
Bidder 3: 	 	 0.00

GSP:

Position 0: 	 bidder 0
Position 1: 	 bidder 1
Position 2: 	 bidder 2
Position 3: 	 bidder 3

Bidder 0: 	 	 4.00
Bidder 1: 	 	 2.00
Bidder 2: 	 	 1.00
Bidder 3: 	 	 0.00

Balanced bids:

Bidder 0: 	 	 10.00
Bidder 1: 	 	 1.70
Bidder 2: 	 	 1.44
Bidder 3: 	 	 1.00

"""