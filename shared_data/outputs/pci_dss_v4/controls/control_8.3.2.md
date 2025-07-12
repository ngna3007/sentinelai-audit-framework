PCI DSS 4_0_1 Requirement Control 8.3.2

Defined Approach Requirements:
Strong cryptography is used to render all authentication factors unreadable during transmission and storage on all system components.

Customized Approach Objective:
Cleartext authentication factors cannot be obtained, derived, or reused from the interception of communications or from stored data.

Testing Procedures:
Testing Procedure 8.3.2.a: Examine vendor documentation and system configuration settings to verify that authentication factors are rendered unreadable with strong cryptography during transmission and storage.
Testing Procedure 8.3.2.b: Examine repositories of authentication factors to verify that they are unreadable during storage.
Testing Procedure 8.3.2.c: Examine data transmissions to verify that authentication factors are unreadable during transmission.

Guidance:
Purpose: Network devices and applications have been known to transmit unencrypted, readable authentication factors (such as passwords and passphrases) across the network and/or store these values without encryption. as a result, a malicious individual can easily intercept this information during transmission using a “sniffer,” or directly access unencrypted authentication factors in files where they are stored, and then use this data to gain unauthorized access.