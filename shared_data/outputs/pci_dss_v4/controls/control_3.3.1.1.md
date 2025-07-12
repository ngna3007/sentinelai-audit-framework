PCI DSS 4_0_1 Requirement Control 3.3.1.1

Defined Approach Requirements:
The full contents of any track are not stored upon completion of the authorization process.

Customized Approach Objective:
This requirement is not eligible for the customized approach.

Applicability Notes:
In the normal course of business, the following data elements from the track may need to be retained: Cardholder name. Primary account number (PAN). Expiration date. Service code. To minimize risk, store securely only these data elements as needed for business.

Testing Procedures:
Testing Procedure 3.3.1.1: Examine data sources to verify that the full contents of any track are not stored upon completion of the authorization process.

Guidance:
Purpose: If full contents of any track (from the magnetic stripe on the back of a card if present, equivalent data contained on a chip, or elsewhere) is stored, malicious individuals who obtain that data can use it to reproduce payment cards and complete fraudulent transactions. Examples: Data sources to review to ensure that the full contents of any track are not retained upon completion of the authorization process include, but are not limited to: incoming transaction data. all logs (for example, transaction, history, debugging, error). history files. trace files. database schemas. contents of databases, and on-premise and cloud data stores. any existing memory/crash dump files. Definitions: Full track data is alternatively called full track, track, track 1, track 2, and magnetic-stripe data. each track contains a number of data elements, and this requirement specifies only those that may be retained post-authorization.