/** Format API decimal strings without converting through binary floats. */
export function formatMoney(amount: string): string {
  const negative = amount.startsWith("-");
  const unsigned = negative ? amount.slice(1) : amount;
  const [wholeRaw, fractionRaw = "00"] = unsigned.split(".");
  const whole = wholeRaw.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  const fraction = fractionRaw.padEnd(2, "0").slice(0, 2);
  const body = `${whole}.${fraction}`;
  return negative ? `(${body})` : body;
}

export function formatPeriod(start: string, end: string): string {
  return `${start} to ${end}`;
}
