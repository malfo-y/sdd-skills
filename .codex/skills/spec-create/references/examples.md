# Spec Document Examples

Use the examples to choose document shape, not to copy every section blindly.

## Which Example to Open

- `examples/simple-project-spec.md`
  - small project
  - 1-3 major components
  - one main spec is enough
  - mostly MUST sections, with optional sections omitted unless clearly useful

- `examples/complex-project-spec.md`
  - larger repository
  - multiple bounded components or services
  - main spec should behave like an index and change map
  - includes selected OPT sections because they materially help navigation

## What to Learn From the Examples

- how the `Goal` section gives a fast repository summary
- how `Architecture Overview` includes both repository map and runtime map
- how `Component Details` starts with a component index before deeper detail
- how optional sections appear only when they add real maintenance value
- how `Usage Examples` includes change/debug entry points, not only run commands
- how `Open Questions` keeps uncertainty explicit

## What Not to Copy

- do not duplicate code structure line by line
- do not include optional sections unless they matter
- do not keep empty metadata or placeholder optional sections
- do not write long narrative when a path table is clearer
- do not hide weak assumptions; move them to `Open Questions`

## Recommended Reading Order

1. Open the simple example for the baseline structure.
2. Open the complex example to see how index-first specs scale.
3. Use `references/template-full.md` for the actual draft.
4. Use `references/optional-sections.md` only when the project needs extra appendices.
