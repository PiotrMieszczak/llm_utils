<!--- Summarise the change in the Title above. -->

## Description
<!--- What changed. Name the plugin and skill(s) affected. -->

## Motivation and Context
<!--- Why is this change required? What problem does it solve? -->
<!--- For a new skill: what does it do that a built-in, a community skill, or an -->
<!--- existing skill here does not? Overlap is the main reason to reject an addition. -->

## Related Issue
<!--- Link any related issue. Optional - not every change needs one. -->

Closes #

## Type of Change
<!--- Put an `x` in all the boxes that apply. -->

- [ ] New skill
- [ ] New plugin
- [ ] Skill improvement (clearer instructions, better triggering, new references)
- [ ] Hook change (behaviour, matcher, or exit semantics)
- [ ] Bug fix
- [ ] Documentation
- [ ] Breaking change (renames a skill, changes a plugin name, or alters hook behaviour)

## Affected Plugins

- [ ] `adr`
- [ ] `frontend-toolkit`
- [ ] `delegation`
- [ ] Marketplace manifest / repository-level

## Validation
<!--- Run these and paste anything that failed. -->

- [ ] All JSON parses (`marketplace.json`, every `plugin.json`, `hooks.json`)
- [ ] Every `source` path in `marketplace.json` resolves to a directory containing
      `.claude-plugin/plugin.json`
- [ ] Skill frontmatter has **only** `name` and `description` (plus `allowed-tools` if
      genuinely needed) — no `execution_model`, `ultrathink`, or other ignored keys
- [ ] Skill `name` matches its directory name and collides with nothing else in the repo
      or with a Claude Code built-in
- [ ] `description` says both *what it does* and *when to use it* — this is what the
      model matches against
- [ ] Internal links resolve
- [ ] Installed locally and the skill triggered on a realistic prompt

```bash
# quick structural check
python3 - <<'EOF'
import json, os, glob
m = json.load(open('.claude-plugin/marketplace.json'))
for p in m['plugins']:
    assert os.path.isfile(os.path.join(p['source'], '.claude-plugin', 'plugin.json')), p['name']
names = [l.split(':',1)[1].strip() for f in glob.glob('plugins/*/skills/*/SKILL.md')
         for l in open(f) if l.startswith('name:')]
assert len(names) == len(set(names)), f"duplicate skill names: {names}"
print("OK", len(m['plugins']), "plugins,", len(names), "skills")
EOF
```

## Hook Changes
<!--- Delete this section if no hook changed. Hooks run on every matching event, -->
<!--- so a broken one degrades every session that installs the plugin. -->

- [ ] Exits `0` on malformed or empty stdin
- [ ] Exits `0` when its state directory is unwritable
- [ ] Cannot loop — honours `stop_hook_active` and consumes its marker before blocking
- [ ] Silent when it has nothing to say (no output on the common path)
- [ ] Tested by piping representative JSON payloads directly to the script

Paste the payloads you tested with and the exit codes you observed:

```
$ echo '{"session_id":"t","cwd":"/tmp"}' | ./hooks/check_adrs.py; echo "exit=$?"
```

## Checklist

- [ ] Self-reviewed the diff
- [ ] Skill instructions are specific and actionable — no vague "be helpful" filler
- [ ] Plugin `README.md` updated if behaviour changed
- [ ] Root `README.md` updated if a plugin or skill was added, renamed, or removed
- [ ] Provenance noted in the root README for any migrated or adapted skill, including
      its source and what was changed
- [ ] No secrets, API keys, or personal paths in the diff

## Notes for Reviewers
<!--- Anything you want a second opinion on, or follow-up work you deliberately deferred. -->
