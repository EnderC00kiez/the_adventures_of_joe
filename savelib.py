table = []
import pickle
import hashlib

def add(string):
	table.append(string)
def append(string, savename):
	with open(savename, "rb") as savefile:
		loaded = pickle.load(savefile)
	loaded.append(string)
	with open(savename, "wb") as savefile:
		pickle.dump(loaded, savefile, protocol=None)
def save(savename):
	with open(savename, "wb") as savefile:
		pickle.dump(table, savefile, protocol=None)
def load(savename):
	with open(savename, "rb") as savefile:
		loaded = pickle.load(savefile)
		return loaded

def loadslot(slot, savename):
	iteration = 0
	for i in load(savename):
		iteration = iteration + 1
		if iteration == slot:
			return i

def gethash(string):
	h = hashlib.new('sha512_256')
	h.update(string.encode("utf8"))
	return h.hexdigest()

def savehashed(savename, hashsavename):
	with open(hashsavename, "w") as hashsave:
		save(savename)
		hashsave.write(gethash(str(table)))
def loadhashed(hashfile, savename):
	with open(hashfile, "r") as hashsave:
		if hashsave.read() == gethash(str(load(savename))):
			return load(savename)
		else:
			raise RuntimeError("Hashes don't match")
def loadslothashed(hashfile, savename, slot):
		with open(hashfile, "r") as hashsave:
			if hashsave.read() == gethash(str(load(savename))):
				return loadslot(slot, savename)
			else:
				raise RuntimeError("Hashes don't match")
def appendhashed(string, savename, hashfile):
	with open(hashfile, "rb") as hashsave:
		if hashsave.read() == gethash(str(load(savename))):
			append(string, savename)
		else:
			raise RuntimeError("Hashes don't match")