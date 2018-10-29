import os
import time
import subprocess
import pickle


lxcPath="/var/lib/lxc/"
updateInterval=300


def calculate_latency(log, objective):
	cmd = "grep 'startTime\|endTime' %s/serverLog | grep --no-group-separator -B1 ^'endTime' | awk '{s=$2;getline;print $2-s;next}'" % log
	latency = subprocess.check_output(cmd, shell=True).rstrip('\n').split('\n')
	computeLatency = sum(map(float, latency)) / len(latency)
    violationRate =  sum(float(i) > float(objective) for i in latency) / len(latency)
	return computeLatency, violationRate

def monitor():
    if os.path.exists("lxcList.txt"):
        with open("lxcList.txt", "rb") as records:
            lxcList = pickle.load(records)
        for lxc in lxcList:
            if not lxc.get('Status'):
                lxc['Status'] = 'off'
            if lxc['Status'] == 'on':
                logPath = lxcPath + "%s/rootfs/root/%s-edgeserver" % (lxc['App'][0], lxc['App'][0].lower())
                lxc['computeLatency'], lxc['violationRate'] = calculate_latency(logPath, lxc['Objective'][0])
                lxc['Requests'] = subprocess.check_output('bash checkLog.sh %s request' % logPath, shell=True)
                lxc['Data'] = subprocess.check_output('bash checkLog.sh %s data' % logPath, shell=True)
                lxc['User'] = subprocess.check_output('bash checkLog.sh %s user' % logPath, shell=True)
                # reset log for next round
                subprocess.check_output('bash checkLog.sh %s reset' % logPath, shell=True)
                # initialise Reward
                if not lxc.get('Reward'):
                    lxc['Reward'] = 0
        # update record
        with open("lxcList.txt",'wb') as wfp:
            pickle.dump(lxcList, wfp)


if __name__ == "__main__":
    while True:
        monitor()
        time.sleep(updateInterval)
