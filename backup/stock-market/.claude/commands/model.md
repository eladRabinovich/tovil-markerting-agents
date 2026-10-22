---
description: בונה מודל אקסל להערכת שווי (5 גיליונות) מהדוחות הכספיים
argument-hint: <TICKER> <paths to financial statements>
---
Use the `financial-modeler` subagent. Company and statements: $ARGUMENTS
If `reports/<TICKER>/` has no market-researcher report, say so and ask whether to run `/research` first.
