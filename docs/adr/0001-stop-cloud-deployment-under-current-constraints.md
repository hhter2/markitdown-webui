---
status: accepted
---

# Stop cloud deployment under the current constraints

Do not implement or deploy the document conversion service under the current constraints. The service would have to run without a local machine, use only free Cloudflare and optionally Supabase services, execute native `markitdown[all]`, retain no data anywhere, and safely process documents; the available runtimes cannot satisfy these requirements together.

## Reasons

- Cloudflare Workers Free does not provide a general Linux or CPython host. Its limits include 10 ms of CPU time per request, 128 MB of memory, and a 3 MB compressed Worker bundle, which are unsuitable for the native dependencies and resource demands of full document conversion.
- Supabase hosted Edge Functions run TypeScript in a Deno-compatible runtime rather than CPython. Their hosted limits include 2 seconds of CPU time and 256 MB of memory, so Supabase cannot execute native `markitdown[all]` or serve as a general Python container host.
- Supabase Database and Storage are persistent services, not conversion compute. Using them for uploaded files or results would also violate zero persistent retention.
- Installing every MarkItDown extra expands the parser, dependency, and network-capable attack surface. Safely accepting untrusted PDF and Office documents requires isolation, timeouts, memory and CPU quotas, concurrency controls, and strict input limits that the selected free runtimes cannot provide for this workload.
- A managed cloud service cannot honestly guarantee that no data of any kind is ever retained. Cloudflare and Supabase may process or retain necessary request, authentication, network, or security metadata even when the application never stores document content.

## Considered options

- Cloudflare Containers or Sandbox could provide full Linux execution and stronger isolation, but require a paid Workers plan.
- A separate Python or container backend could run MarkItDown, but adding another provider is outside the allowed scope.
- A local conversion service exposed through Cloudflare Tunnel could preserve the current Python runtime, but relying on a local machine is not allowed.
- Browser-side conversion could remain free and avoid server retention, but would not provide native `markitdown[all]` or equivalent format support.

## Revisit when

Reconsider implementation only if at least one constraint changes: paid isolated container compute becomes acceptable; a local or external Python backend is allowed; native MarkItDown and full format support are no longer required; or the privacy requirement permits unavoidable provider metadata while still prohibiting persistent document content.

## Sources

- [Cloudflare Workers limits](https://developers.cloudflare.com/workers/platform/limits/)
- [Cloudflare Python package support](https://developers.cloudflare.com/workers/languages/python/packages/)
- [Cloudflare Sandbox security model](https://developers.cloudflare.com/sandbox/concepts/security/)
- [Supabase Edge Functions runtime](https://supabase.com/docs/guides/functions/quickstart)
- [Supabase Edge Functions limits](https://supabase.com/docs/guides/functions/limits)
- [Supabase logs](https://supabase.com/docs/guides/telemetry/logs)
