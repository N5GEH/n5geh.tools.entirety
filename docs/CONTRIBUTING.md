# Entirety contribution guidelines

Thank you for investing your time in contributing to our project!
Please read our contribution guideline carefully.

## Ground rules & expectations

Before we get started, here are a few things we expect from you (and that you should expect from others):

- Be kind and thoughtful in your conversations around this project. We all come from different backgrounds and projects, which means we likely have different perspectives on "how open source is done." Try to listen to others rather than convince them that your way is correct.
- If you open a pull request, you must sign the [Individual Contributor License Agreement](Entirety%20Individual%20Contributor%20License%20Agreement_DRAFT.pdf) by stating in a comment "I have read the CLA Document and I hereby sign the CLA"
- Please ensure that your contribution passes all tests. If there are test failures, you will need to address them before we can merge your contribution.
- When adding content, please consider if it is widely valuable. Please don't add references or links to things you or your employer have created as others will do so if they appreciate it.
- When reporting a vulnerability on the software, please, get in contact with the Entirety repository maintainers in order to discuss it in a private way.

## How to contribute 

If you like to contribute, start by searching through the [issues](https://github.com/N5GEH/n5geh.tools.entirety/issues), [discussions](https://github.com/N5GEH/n5geh.tools.entirety/discussions), and [pull requests](https://github.com/N5GEH/n5geh.tools.entirety/pulls) of this project to see whether someone else has raised a similar idea or question.

1. Open a new [issue](https://github.com/N5GEH/n5geh.tools.entirety/issues) for feature requirement or bug resolution.
2. Assign a user to that issue.
3. Create a new branch for the corresponding issue (you can use the button/link on issue page to create the new branch).
4. Make changes to that branch. Follow the [conventional commits convention](#conventional-commits).
5. Open a [pull request](https://github.com/N5GEH/n5geh.tools.entirety/pulls) **from the new branch to development branch**.
6. Assign reviewer from the list of reviewers.
7. Once the pull request is approved by at least one reviewer, merge the branch to development, test if development branch is working as expected, and delete the old branch.
8. An updated docker image of the development branch will be automatically pushed to the package registry when development branch is updated.

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