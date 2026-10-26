# Mandatory Skill Compliance

Every agent operating in this subtree must read `SKILL.md` and `references/tool-usage.md` completely before performing Riftbound card or deck work.

The required sequence is `doctor` -> exact-code `card --json` resolution -> `retrieve --legend CODE` returning IDs, then `card CODE --json` to inspect full `effect_effective` for chosen candidates -> canonical deck JSON -> successful `validate` -> `export`.

The local CLI and database are the source of truth. Do not substitute memory, web search, copied deck lists, or computer-use. Do not use `--allow-invalid` unless the user explicitly requests an illegal or incomplete draft. Do not present a deck as complete or legal without successful current-task validation and the rules profile's `as_of` date.

The final response must provide style, win condition, operating plan, core cards with reasons, validation profile/date, and RiftAtlas output or file link.
