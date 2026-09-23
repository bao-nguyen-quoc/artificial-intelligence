# Type

- [ ] Documentation (add or update documentation)
- [ ] Bug fix (non-breaking change which fixes an anomaly)
- [ ] Minor Enhancement (non-breaking change which adds or improves small functionality)
- [ ] Major Enhancement (non-breaking change which adds new or big functionality)
- [ ] Breaking change (Any change that would cause existing functionality to not work as expected)

# Description

## What

> Explain the changes you've made here

## Why

> Tells us what business or engineering goal of these changes.

## How

> Describe your significant design / technical decisions.

## Testing

> 1. Explain to the reviewer how to test it locally (if necessary).
> 2. Showing the results of tests (if necessary).
> 3. Let the reviewer know if some conditions or edge cases were not tested, why they weren't tested, and how likely they to occur, and if so, any associated risks.

## Others

> You may want to delve into possible architecture changes or technical debt here. Call out challenges, optimizations, etc.

# Checklist

- [ ] My **code works** in my local machine and **meets all requirements**.
- [ ] **Edge cases and potential error scenarios are handled** appropriately.
- [ ] My code is **well-formatted**, **well organized**, **easy to read** and **follows the coding conventions** of this project.
- [ ] I have **added comments** to explain complex or non-obvious code segments appropriately.
- [ ] My changes generate **no new warnings**.
- [ ] I **have added unit tests** to ensure my code runs properly.
- [ ] New and existing **unit tests are passed locally** with my changes.
- [ ] I have **considered performance bottlenecks or inefficiencies and memory leaks** when coding.
- [ ] I have **selected the corresponding merge strategy**.

---

Make sure you will commit with correct [semantic rules](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716):

- **feat**: (new feature for the user)
- **feat!**: (breaking changes, new feature for the user)
- **fix**: (bug fix for the user)
- **fix!**: (breaking changes, bug fix for the user)
- **docs**: (changes to the documentation)
- **style**: (formatting, missing semi colons, etc; no production code change)
- **refactor**: (refactoring production code, eg. renaming a variable)
- **test**: (adding missing tests, refactoring tests; no production code change)
- **chore**: (updating grunt tasks etc; no production code change)