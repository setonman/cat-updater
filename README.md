# Cat Updater

A tiny Python utility that updates a cat record stored as JSON.

## What it does

- Merges update fields into an existing cat object.
- Rejects changes to immutable fields (`id`, `created_at`).
- Removes fields when an update value is `null`.

## CLI usage

```bash
python cat_updater.py path/to/current.json path/to/updates.json
```

Optionally write output to a file:

```bash
python cat_updater.py current.json updates.json --output updated.json
```

## Example

`current.json`

```json
{
  "id": "cat-42",
  "name": "Mochi",
  "age": 3
}
```

`updates.json`

```json
{
  "name": "Mochi Prime",
  "age": 4,
  "favorite_food": "salmon"
}
```

Output:

```json
{
  "age": 4,
  "favorite_food": "salmon",
  "id": "cat-42",
  "name": "Mochi Prime"
}
```
