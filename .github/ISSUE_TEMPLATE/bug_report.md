name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thank you for helping us improve pyHWM14! Please provide details about the bug.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: What is the bug? What did you expect to happen?
      placeholder: "Expected X, but got Y"
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Minimal Reproducible Example
      description: Provide a minimal code snippet that reproduces the issue
      placeholder: |
        ```python
        from pyhwm2014 import HWM14
        # Your code here
        ```
    validations:
      required: true

  - type: textarea
    id: error
    attributes:
      label: Error Output
      description: Full error message and stack trace (if applicable)
      placeholder: |
        ```
        Traceback (most recent call last):
          ...
        ```

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: System and package information
      placeholder: |
        - OS: [e.g., Ubuntu 24.04, macOS 13, Windows 11]
        - Python version: 3.X
        - pyhwm2014 version: 1.X.X
        - NumPy version: 1.X.X
      value: |
        - OS:
        - Python version: 
        - pyhwm2014 version:
        - NumPy version:
    validations:
      required: true

  - type: checkboxes
    id: checks
    attributes:
      label: Pre-submission Checks
      options:
        - label: I have searched existing issues to avoid duplicates
          required: true
        - label: I can reproduce the issue with the minimal example
          required: true
        - label: I am using Python 3.13 or later
          required: true
