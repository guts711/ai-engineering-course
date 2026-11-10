# FastAPI concept reference — Product Catalog

Use alongside [Session 01](session-01.md) and [Session 02](session-02.md).

| Concept | Product example | General pattern |
|---|---|---|
| Resource | Product | A thing the API represents |
| Collection | `/products` | List/filter resources |
| Path input | `/products/1` | Identify one resource |
| Query input | `?category=books` | Modify selection or retrieval |
| Body input | JSON sent to POST | Supply structured data |
| Request model | `ProductCreate` | Validate incoming structure |
| Response model | `ProductRead` | Define returned data |
| Application error | Missing product → 404 | Handle expected failure |
| State | Product dictionary | Store application data |
| Test | Create, then GET | Check behavior reproducibly |

## Request flow

Client sends method/path/headers/body → Uvicorn receives HTTP → FastAPI matches operation and validates inputs → application function runs → output model validates/filters where configured → JSON response.

## Statuses in our contract

200 reads/replacements; 201 creation; 204 deletion with no body; 404 missing route/resource; 405 unsupported method; 422 invalid declared input. Unexpected exceptions and invalid server output are server failures; do not turn every exception into 200 or 422.

## Distinctions to understand

- GET and POST may share a path because method plus path identifies the operation.
- `None` can mean a query filter was omitted; `False` is a real requested value.
- A nullable Pydantic field is not automatically omittable; an explicit default matters.
- Validation can include type conversion. It does not establish meaningful names, truth, or permission.
- PUT here requires a full representation and preserves the ID; PATCH would need separate partial-update rules.
- Response filtering demonstrates an output contract; it does not grant or check access.
- In-memory state disappears on restart/reload, and each worker would have its own copy. The counter is a teaching mechanism, not concurrent database ID allocation.
- Float prices keep the example short. Real financial values need a deliberate representation and rounding policy.
- We use ordinary `def` functions for this in-memory example. Async I/O is a later topic; adding `async` alone does not make blocking work concurrent.

## Transfer the pattern

When moving from products to tasks or documents, ask: What identifies the resource? What can the client submit? What does the server generate? Which values are valid? What happens if it does not exist? What evidence proves it works?

Official references: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/), [response models](https://fastapi.tiangolo.com/tutorial/response-model/), [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/).
