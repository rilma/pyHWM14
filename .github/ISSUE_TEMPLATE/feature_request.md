name: Feature Request
description: Suggest an idea or enhancement
labels: ["feature"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Great ideas welcome! Please describe your feature request.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: What feature would you like to see?
      placeholder: "It would be great if pyHWM14 could..."
    validations:
      required: true

  - type: textarea
    id: use_case
    attributes:
      label: Use Case
      description: Why do you need this feature? What problem does it solve?
      placeholder: "This would help because..."
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Any alternative approaches you've considered?
      placeholder: "Other solutions I thought about..."

  - type: textarea
    id: additional
    attributes:
      label: Additional Context
      description: Any other relevant information?
      placeholder: "Links to related discussions, papers, examples, etc."

  - type: checkboxes
    id: checks
    attributes:
      label: Pre-submission Checks
      options:
        - label: I have searched existing issues to avoid duplicates
          required: true
        - label: This would be useful for multiple users, not just my use case
          required: false
