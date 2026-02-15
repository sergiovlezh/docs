# Domain Model

## Document

The main logical entity — what the user sees and manages.

- Belongs to a user
- Has a title (derived from the first uploaded file by default) and a description
- Related to one or more files, notes, and tags

## DocumentFile

Represents a physical file stored in the system.

- A document can have multiple files (e.g. pages or attachments)
- The original filename comes directly from storage — it is not duplicated in the model

This separation keeps documents as business concepts independent from storage details.

## DocumentNote

Free-form text created by a user, associated to a document.

## Tag

Global entities, unique by name, used to organize documents.

## DocumentTag

Explicit many-to-many relationship between a document and a tag, including:

- Document
- Tag
- The user who assigned the tag
- A color for the tag

Each (document, tag, user) combination is unique. This allows different users to tag the same document independently, avoids tag duplication, and supports system-defined tags.
