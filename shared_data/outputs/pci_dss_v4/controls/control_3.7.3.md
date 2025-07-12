PCI DSS 4_0_1 Requirement Control 3.7.3

Defined Approach Requirements:
Key-management policies and procedures are implemented to include secure storage of cryptographic keys used to protect stored account data.

Customized Approach Objective:
Cryptographic keys are secured when stored.

Testing Procedures:
Testing Procedure 3.7.3.a: Examine the documented key-management policies and procedures for keys used for protection of stored account data to verify that they define secure storage of cryptographic keys.
Testing Procedure 3.7.3.b: Observe the method for storing keys to verify that keys are stored securely.

Guidance:
Purpose: Storing keys without proper protection could provide access to attackers, resulting in the decryption and exposure of account data. Good Practice: Data encryption keys can be protected by encrypting them with a key-encrypting key. keys can be stored in a hardware security module (hsm). secret or private keys that can decrypt data should never be present in source code.