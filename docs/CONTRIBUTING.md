# Entirety contribution guidelines

Thank you for investing your time in contributing to our project!
Please read our contribution guideline carefully.

## Conventional commits

We are using [conventional commits](https://www.conventionalcommits.org/)
for automatic release management and changelog creation.
Please format your commit messages according to the standard.

Following commit types will affect the version of the next release:

1. **fix:** a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
2. **feat:** a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
3. **BREAKING CHANGE:** a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.


> **_NOTE:_** Descriptions copied from [official docs](https://www.conventionalcommits.org/en/v1.0.0/#specification)

> **_NOTE:_** Following commit types are also supported but will not affect app's version: _build:, chore:, ci:, docs:,
> style:, test:_

## Naming conventions

### HTML

* **accordion-collapse:** _acc\_c\_\<name\>_
* **accordion-header:** _acc\_h\_\<name\>_
* **dialog:** _dg\_\<name\>_
* **div:** _d\_\<name\>_
* **dropdown:** _dd\_\<name\>_
* **modal**: _m\_\<name\>_
