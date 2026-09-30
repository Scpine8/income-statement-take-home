export function incomeStatementUrl(
  start: string,
  end: string,
  baseUrl: string = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
): string {
  const params = new URLSearchParams({ start, end });
  return `${baseUrl}/income-statement?${params.toString()}`;
}
