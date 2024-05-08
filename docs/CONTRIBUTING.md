# Entirety contribution guidelines

Thank you for investing your time in contributing to our project!
Please read our contribution guideline carefully.

## Conventional commits

We are using [conventional commits](https://www.conventionalcommits.org/)
for automatic release management and changelog creation.
Please format your commit messages according to the standard:
```
<commit type>(<commit scope>): <message>
```
Here is an example, where the commit type is `feat`, the commit scope is `entities`, and the message is `implement new search bar`:
```git
feat(entities): implement new search bar
```

### Commit type
Following commit types will affect the version of the next release:

1. **fix:** a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
2. **feat:** a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
3. **BREAKING CHANGE:** a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.

> **_NOTE:_** Descriptions copied from [official docs](https://www.conventionalcommits.org/en/v1.0.0/#specification)

> **_NOTE:_** Following commit types are also supported but will not affect app's version: _build:, chore:, ci:, docs:,
> style:, test:_

### Commit scope
The commit scope should be the name of the related modules, i.e., one of `entities`, `devices`, `notifications`, `semantics`, and `data models`.

If the commit is not bound to specific modules, for example some changes to the general templates or settings, then `entirety` should be used.

## Naming conventions

### HTML

* **accordion-collapse:** _acc\_c\_\<name\>_
* **accordion-header:** _acc\_h\_\<name\>_
* **dialog:** _dg\_\<name\>_
* **div:** _d\_\<name\>_
* **dropdown:** _dd\_\<name\>_
* **modal**: _m\_\<name\>_

## GitHub Workflow for development

1. Open a new issue for feature requirement or bug resolution.
2. Assign a user to that issue.
3. Create new branch for the corresponding issue (you can use the button/link on issue page to create the new branch).
4. Make changes to that branch.
5. Open a Pull Request from the new branch to development branch.
6. Assign reviewer from the list of Reviewers.
7. Once the Pull Request is approved by at least one reviewer, merge the branch to development, test if development
branch is working as expected and delete the old branch.
8. Updated development docker image will be automatically pushed to package registry when development branch will be updated.
