# ======================== CSV FILE: WHAT YOU HAVE TO DO ========================
# 1. In VS Code, create a NEW FILE in the SAME folder as this .py file.
# 2. Name it  exp2.csv
# 3. Copy the lines below into it (WITHOUT the '# ' at the start), save with Ctrl+S.
#
#    task_id,thread_name,burst_ms,priority,status
#    T1,Worker_1,200,HIGH,PENDING
#    T2,Worker_2,300,LOW,PENDING
#    T3,Worker_3,150,MEDIUM,PENDING
#    T4,Worker_1,100,LOW,PENDING
#    T5,Worker_2,250,HIGH,PENDING
#    T6,Worker_3,120,HIGH,PENDING
#
# RULES: priority must be HIGH, MEDIUM or LOW. burst_ms = a number like 100-300.
#
# 4. Change DOMAIN below to your chit's domain.   5. Run:  python exp2.py
# ===============================================================================

# WHAT THIS PROGRAM DOES (MULTITHREADING WITH A LOCK):
# Every task runs in its own thread (all at the same time).
# All threads write into ONE shared list called "completed".
# The lock makes sure only ONE thread writes at a time -> no race condition.
#   lock.acquire()  = take the lock (others must wait)
#   lock.release()  = give the lock back

import csv
import threading       # lets us run things at the same time
import time            # lets us wait (sleep)

DOMAIN = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change to your chit
FILE = "exp2.csv"                                             # change to your CSV name

lock = threading.Lock()      # the lock
completed = []               # shared list that all threads write into


# this is what every thread does
def worker(task_id, name, burst, priority):
    lock.acquire()
    print(name, "started", task_id, "priority", priority, "time", burst, "ms")
    lock.release()

    time.sleep(burst / 1000)          # pretend to work (sleep wants seconds, so /1000)

    lock.acquire()                    # take the lock before touching the shared list
    print("   ", name, "LOCK ACQUIRED  -", task_id, "COMPLETED")
    completed.append(task_id)
    print("   ", name, "LOCK RELEASED")
    lock.release()                    # give the lock back


print("=== Multithreading for", DOMAIN, "===")
print()

# ---------- read the CSV into a list ----------
tasks = []
file = open(FILE)
for row in csv.DictReader(file):
    tasks.append(row)
file.close()

# ---------- start the threads: HIGH first, then MEDIUM, then LOW ----------
threads = []
for level in ["HIGH", "MEDIUM", "LOW"]:
    for row in tasks:
        if row["priority"] == level:
            t = threading.Thread(target=worker,
                                 args=(row["task_id"], row["thread_name"], int(row["burst_ms"]), level))
            t.start()                 # thread starts running now
            threads.append(t)

# ---------- wait for every thread to finish ----------
for t in threads:
    t.join()

print()
print("Final completed task list:", completed)