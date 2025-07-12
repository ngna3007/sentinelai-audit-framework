PCI DSS 4_0_1 Requirement Control 8.3.6

Defined Approach Requirements:
If passwords/passphrases are used as authentication factors to meet Requirement 8.3.1, they meet the following minimum level of complexity: A minimum length of 12 characters (or IF the system does not support 12 characters, a minimum length of eight characters). Contain both numeric and alphabetic characters.

Customized Approach Objective:
A guessed password/passphrase cannot be verified by either an online or offline brute force attack.

Applicability Notes:
This requirement is not intended to apply to: User accounts on point-of-sale terminals that have access to only one card number at a time to facilitate a single transaction. Application or system accounts, which are governed by requirements in section 8.6. _This requirement is a best practice until 31 March_ _2025, after which it will be required and must be_ _fully considered during a PCI DSS assessment._ Until 31 March 2025, passwords must be a minimum length of seven characters in accordance with PCI DSS v3.2.1 Requirement 8.2.3.

Testing Procedures:
Testing Procedure 8.3.6: Examine system configuration settings to verify that user password/passphrase complexity parameters are set in accordance with all elements specified in this requirement.

Guidance:
Purpose: Strong passwords/passphrases may be the first line of defense into a network since a malicious individual will often first try to find accounts with weak, static, or non-existent passwords. if passwords are short or easily guessable, it is relatively easy for a malicious individual to find these weak accounts and compromise a network under the guise of a valid user id. Good Practice: Password/passphrase strength is dependent on password/passphrase complexity, length, and randomness. passwords/passphrases should be sufficiently complex, so they are impractical for an attacker to guess or otherwise discover its value. entities can consider adding increased complexity by requiring the use of special characters and upper- and lower-case characters, in addition to the minimum standards outlined by this requirement. additional complexity increases the time required for offline brute force attacks of hashed passwords/passphrases. another option for increasing the resistance of passwords to guessing attacks is by comparing proposed password/passphrases to a bad password list and having users provide new passwords for any passwords found on the list.