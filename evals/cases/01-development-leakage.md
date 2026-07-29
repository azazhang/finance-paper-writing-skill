# Case 1: Development Leakage

## Prompt

Revise the data and measurement paragraph for a finance manuscript.

## Draft

> The project combines two locally archived source files. After the release-7 candidate observations are produced, the pipeline merges them onto the final analysis backbone. Generated manuscript exhibits are built from machine-readable outputs with a separate hash manifest.

## Expected Diagnosis

- research-workspace leakage;
- method capture;
- unexplained sample and linkage;
- replication governance mixed into manuscript prose.

## Passing Behavior

Rewrite around named data sources, coverage, observation unit, filtering, linkage, and measure construction. Move versions, hashes, and output provenance to replication records.
