# Consent and data handling

This build stores authenticated account consent and a separate consent record for each request. It is pseudonymous within operational and audit records; it does not claim fully anonymous account registration.

## Collection

The signup notice explains account and reporting use. Each request requires explicit consent. Volunteers also confirm that they explained the notice and obtained the citizen's agreement; they must omit the citizen's name and phone number.

Text processing redacts common phone and email patterns. This is not a comprehensive personal-data detector. Original media is private and image metadata is stripped at upload.

## Public evidence

Only a separately redacted image uploaded and reviewed by an administrator can appear on its linked public project. A record of that action is appended to the audit log. Active account and report consent are checked on every public media request. Originals are never served through the public route. There is no automatic face-blurring model.

## Withdrawal and erasure

Users may withdraw account/report consent in their profile. Account withdrawal prevents new reports. Either account or report withdrawal removes public access to the associated evidence; existing operational records remain available for authorized review.

The erasure action requires the current password and explicit confirmation. It removes identifying profile fields, report text, media and report review notes; report coordinates are reduced to a coarse grid, attribution is removed, and the account is suspended with its sessions invalidated. Anonymous operational rows and opaque audit references remain. Administrator accounts cannot self-erase through this route.

Offline drafts remain in the originating browser until synchronized or explicitly removed. Use the queue's Remove action on a shared device. Server erasure does not erase browser-local drafts or independently downloaded copies.

Backup retention and jurisdiction-specific legal review must be defined before production deployment. This implementation is not a legal-compliance certification.
