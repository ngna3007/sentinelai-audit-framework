PCI DSS 4_0_1 Requirement Control 8.3.7

Defined Approach Requirements:
Individuals are not allowed to submit a new password/passphrase that is the same as any of the last four passwords/passphrases used.

Customized Approach Objective:
A previously used password cannot be used to gain access to an account for at least 12 months.

Applicability Notes:
This requirement is not intended to apply to user accounts on point-of-sale terminals that have access to only one card number at a time to facilitate a single transaction.

Testing Procedures:
Testing Procedure 8.3.7: Examine system configuration settings to verify that password parameters are set to require that new passwords/passphrases cannot be the same as the four previously used passwords/passphrases.

Guidance:
Purpose: If password history is not maintained, the effectiveness of changing passwords is reduced, as previous passwords can be reused over and over. requiring that passwords cannot be reused for a period reduces the likelihood that passwords that have been guessed or brute-forced will be re- used in the future. passwords or passphrases may have previously been changed due to suspicion of compromise or because the password or passphrase exceeded its effective use period, both of which are reasons why previously used passwords should not be reused.