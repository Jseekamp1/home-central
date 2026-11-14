export interface ApiResult<T> {
  data: T | null
  error: string | null
  status: number
}

interface ValidationIssue {
  loc: (string | number)[]
  msg: string
}

function isValidationIssue(value: unknown): value is ValidationIssue {
  return typeof value === 'object' && value !== null && 'loc' in value && 'msg' in value
}

// FastAPI sends `detail` as a string for HTTPExceptions and as a list of
// issues for request validation errors (422).
function describeError(body: unknown): string {
  const detail = typeof body === 'object' && body !== null && 'detail' in body
    ? (body as { detail: unknown }).detail
    : undefined

  if (typeof detail === 'string') return detail

  if (Array.isArray(detail)) {
    const messages = detail.filter(isValidationIssue).map((issue) => {
      const field = issue.loc.filter(part => part !== 'body').join('.')
      return field ? `${field}: ${issue.msg}` : issue.msg
    })
    if (messages.length > 0) return messages.join('; ')
  }

  return 'Request failed'
}

export function useApi(baseUrl: string = useRuntimeConfig().public.apiBase) {
  async function request<T>(path: string, init: RequestInit = {}): Promise<ApiResult<T>> {
    let response: Response
    try {
      response = await fetch(`${baseUrl}${path}`, {
        ...init,
        headers: { 'Content-Type': 'application/json', ...init.headers },
      })
    }
    catch {
      return { data: null, error: 'Could not reach the server', status: 0 }
    }

    const { status } = response

    if (!response.ok) {
      const body: unknown = await response.json().catch(() => null)
      return { data: null, error: describeError(body), status }
    }

    if (status === 204) return { data: null, error: null, status }

    return { data: (await response.json()) as T, error: null, status }
  }

  return { request }
}
