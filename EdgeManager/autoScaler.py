import pickle
import time
import os
from terminater import terminate
from edgeManager import has_enough_resource
from operator import itemgetter
import subprocess
import psutil

scaleInterval=600
networkLatency=5.689 # Average ping time between Edge node and users measured beforehand
unitCPU = 1000000       # 1 core
unitMemory = 256        # MB
pmApproach = "SPS"      # Priority management approach, choose from "SPS", "wDPS", "cDPS", "sDPS"
priceModel = "PFP"      # Pricing model, choose from "PFP", "PFR", "Hybrid"

def scale_up(appName, sortedRunning, record):
    # measure current allocation
    cmdCPU = "lxc-cgroup -n %s cpu.cfs_quota_us" % appName
    cmdMemory = "lxc-cgroup -n %s memory.limit_in_bytes)/1024/1024" % appName
    currentCPU = float(subprocess.check_output(cmdCPU, shell=True))
    currrentMemory = float(subprocess.check_output(cmdMemory, shell=True))
    # only act if lxc has not been allocated the maximum resources
    if currentCPU < psutil.cpu_count() and currrentMemory < psutil.virtual_memory().total:
        # calculate resources to add
        indApp, lxc = next(((index, d) for (index, d) in enumerate(record) if d['App'][0] == appName), None)
        cpu2Add = currentCPU * record[indApp]['violationRate']
        memory2Add = currrentMemory * record[indApp]['violationRate']
        if has_enough_resource(cpu2Add, memory2Add):
            # add required resource to the app container
            os.system('lxc-cgroup -n %s cpu.cfs_quota_us %s' % (appName, currentCPU + cpu2Add))
            os.system('lxc-cgroup -n %s memory.limit_in_bytes %sM' % (appName, currrentMemory + memory2Add))
            # update Scale in registry
            if record[indApp]['Scale']:
                record[indApp]['Scale'] += 1
            else:
                record[indApp]['Scale'] = 1
        else:
            # terminate other containers from the one with lowest priority
            while not has_enough_resource(cpu2Add, memory2Add) and len(sortedRunning) > 1:
                terminate(sortedRunning[-1])
                # update status in registry
                ind = next((index for (index, d) in enumerate(record) if d['App'] == sortedRunning[-1]['App']), None)
                record[ind]['Status'] = 'off'
                # remove this lxc from sorted list
                del sortedRunning[-1]
            if has_enough_resource(cpu2Add, memory2Add):
                # add required resource to the app container
                os.system('lxc-cgroup -n %s cpu.cfs_quota_us %s' % (appName, currentCPU + cpu2Add))
                os.system('lxc-cgroup -n %s memory.limit_in_bytes %sM' % (appName, currrentMemory + memory2Add))
                # update Scale in registry
                if record[indApp]['Scale']:
                    record[indApp]['Scale'] += 1
                else:
                    record[indApp]['Scale'] = 1
            else:
                print "Scaling up aborted, lack of resources."
    else:
        print "Scaling up aborted, maximum resources allocated already."



def scale_down(appName, record):
    # measure current allocation
    cmdCPU = "lxc-cgroup -n %s cpu.cfs_quota_us" % appName
    cmdMemory = "lxc-cgroup -n %s memory.limit_in_bytes)/1024/1024" % appName
    currentCPU = float(subprocess.check_output(cmdCPU, shell=True))
    currrentMemory = float(subprocess.check_output(cmdMemory, shell=True))
    # only act if lxc has not been allocated the minimum resources
    if currentCPU > unitCPU and currrentMemory > unitMemory:
        # remove one unit of resource from the app container
        os.system('lxc-cgroup -n %s cpu.cfs_quota_us %s' % (appName, currentCPU - unitCPU))
        os.system('lxc-cgroup -n %s memory.limit_in_bytes %sM' % (appName, currrentMemory - unitMemory))
        # update Scale in registry
        indApp = next((index for (index, d) in enumerate(record) if d['App'][0] == appName), None)
        if record[indApp]['Scale']:
            record[indApp]['Scale'] += 1
        else:
            record[indApp]['Scale'] = 1
    else:
        print "Scaling down aborted as minimum resource reached."


def calculate_ps(lxc):
    if pmApproach == 'SPS':
        ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty'])
    if pmApproach == 'wDPS':
        if priceModel == 'PFP':
            ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty']) + 1/float(lxc['Requests']) + 1/float(lxc['Users']) + 1/float(lxc['Data'])
        else:
            ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty']) + lxc['Requests'] + lxc['Users'] + lxc['Data']
    if pmApproach == 'cDPS':
        if priceModel == 'PFP':
            ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty']) + 1/float(lxc['Requests']) + 1/float(lxc['Users']) + 1/float(lxc['Data']) + lxc['Reward']
        else:
            ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty']) + lxc['Requests'] + lxc['Users'] + lxc['Data'] + lxc['Reward']
    if pmApproach == 'sDPS':
        # initalise scale factor
        if not lxc.get('Scale'):
            lxc['Scale'] = 1
        if priceModel == 'PFP':
            ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty']) + 1/float(lxc['Requests']) + 1/float(lxc['Users']) + 1/float(lxc['Data']) + lxc['Reward'] + 1/float(lxc['Scale'])
        else:
            ps = lxc['Aging'] + 1/float(lxc['ID']) + float(lxc['Premium'][0]) + float(lxc['Loyalty']) + lxc['Requests'] + lxc['Users'] + lxc['Data'] + lxc['Reward'] + 1/float(lxc['Scale'])
    return ps


def auto_scale():
    if os.path.exists("lxcList.txt"):
        with open("lxcList.txt", 'rb') as f:
            lxcList = pickle.load(f)
        # scale running LXC only
        runningLXC = [d for d in lxcList if d['Status'] == 'on']
        if len(runningLXC) > 0:
            print "%d LXCs to scale" % len(lxcList)
            if pmApproach == "SPS":
                for lxc in runningLXC:
                    if not lxc.get('Priority'):
                        lxc['Priority'] = calculate_ps(lxc)
            else:
                for lxc in runningLXC:
                    lxc['Priority'] = calculate_ps(lxc)
            # sort by priority
            sortedLXC = sorted(runningLXC, key=itemgetter('Priority'), reverse=True)
            for lxc in sortedLXC:
                ind = next((index for (index, d) in enumerate(lxcList) if d['App'] == lxc['App']), None)
                # check activeness
                if lxc['Requests'] > 0 and networkLatency < float(lxc['Objective'][0]):
                    print "Scaling %s" % lxc['App'][0]
                    appLatency = networkLatency + lxc['computeLatency']
                    if appLatency > float(lxc['Objective'][0]):
                        scale_up(lxc['App'][0], sortedLXC, lxcList)
                    elif appLatency > float(lxc['Threshold'][0]) * float(lxc['Objective'][0]):
                        if lxc['Donation'][0] == 'Yes':
                            scale_down(lxc['App'][0], lxcList)
                            # update Reward in registry
                            lxcList[ind]['Reward'] += 1
                    else:
                        scale_down(lxc['App'][0], lxcList)
                else:
                    print "App %s will be terminated due to inactivity or long network delay." % lxc['App']
                    terminate(lxc)
                    # update status in registry
                    lxcList[ind]['Status'] = 'off'
                    # remove this lxc from sorted list
                    del sortedLXC[-1]
        else:
            print "No running LXCs to scale."

while True:
    auto_scale()
    time.sleep(scaleInterval)
