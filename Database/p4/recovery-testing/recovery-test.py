import os
from disk_relations import *
from transactions import *
import time
from exampletransactions import *
import sys
import subprocess
import random
import traceback
import shutil

os.remove("recoverytest_logfile") if os.path.exists("recoverytest_logfile") else None
os.remove("student_generated_relation") if os.path.exists("student_generated_relation") else None
bpool = BufferPool()
relationname = "student_generated_relation"
logfile = "recoverytest_logfile"
shutil.copy("recoverytest_logfile_original", logfile)
r = Relation(relationname)
print "Starting to analyze the logfile " + logfile
LogManager.setAndAnalyzeLogFile(logfile)
correctrelationname = "correct_relation"
correctlogfile = "correct_logfile"
success = True
print "Comparing the relations"
rel1 = open(relationname, 'r').read()
rel2 = open(correctrelationname, 'r').read()
if len(rel1) != len(rel2):
	print "The two files are not the same length"
diff1 = ""
diff2 = ""
for i in range(Globals.blockSize, min(len(rel1), len(rel2))):
	if rel1[i] != rel2[i]:
		success = False
		diff1 += rel1[i]
		diff2 += rel2[i]

if not success:
	print "Relations Failed:"
	print "-- Your relation: " + diff1
	print "-- Correct relation: " + diff2

print "Comparing the logfiles"
log1 = open(logfile, 'r').readlines()
log2 = open(correctlogfile, 'r').readlines()

if len(log1) != len(log2):
	print "Logs Failed: different sizes"
for i in range(0, len(log2)):
	if log1[i] != log2[i]:
		print "Logs Failed: Line " + str(i) + " of the correct log is different"
		success = False

if success:
	print "-- PASSED --"
	os._exit(0)
else:
	print "-- FAILED --"
