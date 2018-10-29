# DYVERSE - DYnamic VERtical Scaling in Multi-tenant Edge Environments
The vision of Edge computing is to bring computing towards the edge of the network. Our previous work, [ENORM](https://github.com/qub-blesson/ENORM) facilitates the hosting of services closer to user devices that frequently interact with the Cloud so that communication latencies can be reduced. To improve the Edge Computing serives supported by ENORM, DYVERSE further provides priority-based dynamic resource allocation while supporting multiple Edge applications on an Edge node.

This is a developing research project and some features might not be stable yet.

# License
All source code, documentation, and related artifacts associated with the DYVERSE open source project are licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).

# How to Use
In addition to the [iPokeMon](https://github.com/qub-blesson/ENORM/tree/master/Application) use case supported in ENORM, a real time Face Detection application is also provided to test DYVERSE. The differences between these two uses cases are:
1. FD requires both the Edge and the Cloud servers work together to process requests, whereas iPokeMon requires either the Edge or the Cloud server to process requests.
2. FD does not require a database server, whereas iPokeMon requires a database server.

You will need the code provided in folder *Application* to use the DYVERSE prototype:
1. Follow instructions of Edge Manager in folder *EdgeManager* to set up the Edge node.
2. Follow instructions of Cloud Manager in folder *CloudManager* to request (and terminate) Edge service for FD.
3. Follow instructions of FD Cloud Server in foder *FaceDetection-CloudServer* to set up the Cloud Server
4. Follow instructions of FD Client in folder *FaceDetection-EdgeServer* to set up the streaming camera.

# Citation
Please cite [DYVERSE - DYnamic VERtical Scaling in Multi-tenant Edge Environments](https://arxiv.org/pdf/1810.04608.pdf) when using this project as follows:

N. Wang, B. Varghese, M. Matthaiou, and D. S. Nikolopoulos, "DYVERSE - DYnamic VERtical Scaling in Multi-tenant Edge Environments," arXiv:1810.04608, 2018.  
