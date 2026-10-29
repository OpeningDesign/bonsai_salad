# ifc_dxf — notes

Things that were not obvious, and cost time to find. Each entry is the symptom
first, because that is what you will have when you arrive here.

Add to this file in the same commit that fixes the thing. A bug that took an
afternoon to corner and a line to fix leaves nothing behind otherwise, and the
next person pays for it again.

------

## Annotations

### Resolve a text literal's formulas before its variables, and pass the product

**Symptom:** tag text comes out empty. 40 of 48 annotation ATTRIBs held `''`.

A Bonsai text literal mixes two syntaxes: `{{...}}` variables and
`` ``...`` `` formulas. Substituting the variables first turns

```
``concat({{type.Name}}, " (", substr({{EPset_Status.Status}}, 2, 4), ")")``
```

into `concat(L2, " (", substr(EXISTING, 2, 4), ")")`, and
`ifcopenshell.util.selector.format` then raises
`UnexpectedCharacters: No terminal matches 'L' at col 8` — the substituted
values are bare words where its grammar wants quoted strings.

**Rule:** do what `tool.Drawing.replace_text_literal_variables` does — hand each
formula to `format()` *with the product*, and let it resolve the `{{...}}`
inside, quoting and typing each value the way its own grammar needs. Resolve
whatever `{{...}}` remain afterwards. `format(query, element=None)` takes an
element on both the 0.8 and 0.9 lanes; a comment in this repo once claimed
otherwise and the empty strings followed from believing it.

A list-valued property (`IfcPropertyEnumeratedValue`) resolves to a list, which
needs joining before it reaches a DXF string.

### Only `align_point` (group code 11) positions aligned text

For a TEXT or ATTDEF with a non-default `halign`/`valign` — anything but
left/baseline — DXF readers take the position from group code 11 and ignore
code 10. Set `insert` alone and the text lands at the origin. IFC
`BoxAlignment` maps to those two codes via
`annotations._BOX_ALIGN_TO_TEXT`; note the values are `"top-middle"` and
`"bottom-middle"` but a bare `"center"` for the middle row.
