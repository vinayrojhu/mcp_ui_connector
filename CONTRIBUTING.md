# Contributing

Keep connector actions declarative and finite. Changes to action schemas must update the JSON Schema, Pydantic model, TypeScript types, validator, worker, and documentation together. Avoid logging task inputs, secrets, cookies, or UI field values. Run the documented policy tests before submitting changes.
