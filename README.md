## Overview
The purpose of this repository is to provide a personal data disclosure form template and related tools/scripts.  Each module will specialize and store this form in the top level of their git repository.  The form is a mechanism to disclose the types of personal data stored by each module.  This information enables those hosting FOLIO to better manage and comply with various privacy laws and restrictions, e.g. GDPR, etc.

## How do I use this form?
1. Place a copy of the [PERSONAL_DATA_DISCLOSURE.md](PERSONAL_DATA_DISCLOSURE.md) at the top level of your module's git repository, e.g. next to `README.md`, `NEWS.md`, etc.
2. Fill out the form by adding an `x` in the `[ ]` for each of the fields your module stores, e.g. `[x] First Name`

**N.B.** _All_ modules (including UI) must include a copy of this form in their git repository, even if they don't store any data.  There's a checkbox at the top indicating that this module doesn't store any personal data.  This removes ambiguities around whether the module doesn't store personal data, or if the module developers simply haven't filled it out yet, etc.

## Revision Control
The disclosure form is versioned, with the version indicated at the bottom of the form.  As adjustments are made to the template, this version shall be updated accordingly.  These changes will be submitted as pull requests (PRs) to be reviewed and approved by the code owners of this repository.  Major changes - indicating changes which are not backwards compatible, e.g. removing a field from the list) will result in a new "release" in git.

## Aggregation
Since the specialized/"filled-in" forms will be distributed among each of the module repositories, their individual value is somewhat limited.  An aggregate picture of all or a collection of the modules is much more useful.  Tooling/scripts provided by this repository help with this aggregation.

## FAQ

### Why markdown?
You may be wondering, if the end goal is aggregate these forms, why was an unstructured format like markdown chosen over something like json or xml?  This was a conscious decision made after weighing the merits of various formats.  The main tradeoff is ease of filling the form out vs ease of consumption/aggregation.  When coupled with a template, the markdown approach strikes a good balance.  It's easy to fill out, and human readable w/o a separate presentation layer (e.g. HTML/JS), and is still fairly easy to parse for aggregation purposes.

### Why distribute these forms?
You may also be thinking it seems silly to distribute these just to aggregate them into a single list.  The rationale for this decision is:
* There's a perception that there's a greater chance of teams not keeping the form up-to-date if it lives in a separate repository.
* It allows for third party modules.  If an institution or company wants to write their own version of a module, and keep that codebase separate from folio-org, this would allow them to still disclose the personal data the module stores in the same fashion as the folio-org modules.
* It's easier to enforce compliance.  In theory a PR check could be introduced that ensures that a disclosure form is present.  These checks could even be extended to verify a particular version of the form is used, and that it's actually filled out, not just present.
