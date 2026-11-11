# Homework 02 — Product availability

**Required. Due:** before Session 02. **Time budget:** 45–75 minutes during Wednesday, the single day between sessions.

Extend your own Session 01 Product Catalog. Do not start another application or copy the Session 02 completed solution.

## Required changes

1. Add `in_stock` as a boolean field on products. When omitted from a creation request, it defaults to `true`.
2. Give each seeded product an explicit availability value; ensure there is at least one available and one unavailable product.
3. Add an optional `in_stock` query parameter to `GET /products`:
   - Omitted: do not filter by stock.
   - `true`: return available products only.
   - `false`: return unavailable products only.
4. Combine it with the existing category filter. Both conditions must hold when both filters are supplied.
5. Preserve the name-length constraint (1–120), positive finite price, existing routes, and server-generated IDs.

## Evidence to include

Show the request, observed status, and relevant response for:

| Check | Expected result |
|---|---|
| Create a product without `in_stock` | 201; stored product defaults to true |
| Create a product with `in_stock=false` | 201; false is preserved |
| List without stock filtering | Both stock states can appear |
| Filter `in_stock=false` | Only unavailable products |
| Filter category and stock together | Every returned product satisfies both |
| POST an empty name | 422; no product created |

Manual requests through `/docs` are sufficient for this assignment; automated tests are introduced in Session 02.

## Submission

Keep the catalog under `student-work/YOUR-USERNAME/week-01/catalog/` in your fork. Add a short README with run instructions, evidence, one explanation of omitted versus false, and any blocker. Commit, push to your fork, and open or update a pull request following the [submission guide](../../student-work/README.md). Do not edit the instructor reference.

Be ready to explain your implementation at the beginning of Session 02. If blocked, ask for help and finish the remaining work; practice is required.
