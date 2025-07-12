PCI DSS 4_0_1 Requirement Control 10.6

Defined Approach Requirements:
Time-synchronization mechanisms support consistent time settings across all systems.

Guidance:
Purpose: Time synchronization technology is used to synchronize clocks on multiple systems. when clocks are not properly synchronized, it can be difficult, if not impossible, to compare log files from different systems and establish an exact sequence of events, which is crucial for forensic analysis following a breach. for post-incident forensics teams, the accuracy and consistency of time across all systems and the time of each activity are critical in determining how the systems were compromised. Examples: Network time protocol (ntp) is one example of time-synchronization technology.