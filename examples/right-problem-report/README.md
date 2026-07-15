# Right Problem Report Example

This example renders a bilingual, presentation-only report from `report.json`. It demonstrates how a host can display a completed Right Problem evaluation without changing the Golden Skill contract.

## Safety and scope

- Data is rendered with DOM `textContent`; untrusted values are never inserted as HTML.
- The page contains no solution recommendations or implementation plan.
- `Valid` permits a gated next thinking step; it does not prove objective truth.
- The view model validates against `schemas/right-problem-report.schema.json`.
- Lists are data-driven rather than fixed to a predetermined item count.

Serve this directory through a local static server and open `index.html`. Direct `file://` access may prevent the browser from loading `report.json`.

```bash
python -m http.server 8000 --directory examples/right-problem-report
```

This implementation is original ThinkingOS project code informed by general problem-framing concepts. It does not copy the user-provided prototype markup.
