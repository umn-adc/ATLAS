/**
 * Formats a number to USD
 * @param value  The amount of money
 * @example formatCurrency(2847392) => '$2,847,392'
 */
export function formatCurrency(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);
}

/**
 * Formats a number to USD with a + or - in front
 * @param value  The amount of money
 * @example formatSignedCurrency(2847392) => '+$2,847,392'
 */
export function formatSignedCurrency(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0, signDisplay: 'exceptZero' }).format(value);
}

/**
 * Formats a decimal to a percentage
 * @param value The decimal to format
 * @param digits How many decimal places to have
 * @example formatPercent(0.56, 0) => '56%'
 */
export function formatPercent(value: number, digits = 1): string {
    if (value > 1 || value < -1) throw new Error('Value should be between 0 and 1');

    return Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: digits, signDisplay: 'negative' }).format(value);
}

/**
 * Formats a decimal to a percentage
 * @param value The decimal to format
 * @param digits How many decimal places to have
 * @example formatSignedPercent(0.76) => '+76%'
 */
export function formatSignedPercent(value: number, digits = 1): string {
    if (value > 1 || value < -1) throw new Error('Value should be between 0 and 1');

    return Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: digits, signDisplay: 'exceptZero' }).format(value);
}

/**
 * Formats a number with either + or - in front
 * @param value The number to format
 * @example formatSignedNumber(907) => '+907'
 */
export function formatSignedNumber(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'decimal', signDisplay: 'exceptZero', maximumFractionDigits: 0 }).format(value);
}

/**
 * Formats a price to include the two decimal places
 * @param value The number to format
 * @example formatPrice(5623.5) => '5623.50'
 */
export function formatPrice(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
}

/**
 * Chooses a color based on the value of the price
 * @param value The price to evaluate
 * @returns Either gain, loss, or neutral based on the value of the price
 * @example pnlTone(12) => 'gain'
 */
export function pnlTone(value: number): 'gain' | 'loss' | 'neutral' {
    return value === 0 ? 'neutral' : value > 0 ? 'gain' : 'loss';
}

/**
 * Formats a plain number with thousands separators and a fixed number of decimals (no currency sign)
 * @param value The number to format
 * @param digits How many decimal places to have
 * @example formatNumber(5623.5, 2) => '5,623.50'
 */
export function formatNumber(value: number, digits = 0): string {
    return Intl.NumberFormat('en-US', { style: 'decimal', minimumFractionDigits: digits, maximumFractionDigits: digits }).format(value);
}

/**
 * Formats a P&L amount to USD with a + or - in front. Whole dollars stay whole, anything else shows cents
 * @param value The profit or loss
 * @example formatPnl(3250) => '+$3,250'
 * @example formatPnl(-562.5) => '-$562.50'
 */
export function formatPnl(value: number): string {
    const digits = Number.isInteger(value) ? 0 : 2;

    return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: digits, maximumFractionDigits: digits, signDisplay: 'exceptZero' }).format(value);
}

/**
 * Swaps the keyboard hyphen in front of a negative number for a real minus sign (U+2212).
 * The real minus is as wide as a digit, so negative numbers line up in columns
 * @param text An already formatted number
 * @example minusSign('-3.2%') => '−3.2%'
 */
export function minusSign(text: string): string {
    return text.startsWith('-') ? `−${text.slice(1)}` : text;
}

/**
 * Formats a length of time using its two largest units
 * @param ms The duration in milliseconds
 * @example formatDuration(273_600_000) => '3d 4h'
 * @example formatDuration(2_000) => '2s'
 */
export function formatDuration(ms: number): string {
    const totalSeconds = Math.max(0, Math.floor(ms / 1000));
    const days = Math.floor(totalSeconds / 86_400);
    const hours = Math.floor((totalSeconds % 86_400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);

    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    if (minutes > 0) return `${minutes}m`;
    return `${totalSeconds}s`;
}

/* ---------- Market time ----------
 * Everything on screen is shown in exchange time (US Eastern), no matter where the browser is. */

const MARKET_TIME_ZONE = 'America/New_York';

type DateInput = Date | string | number;

/**
 * Formats a moment as a 24h clock time in Eastern time
 * @param value A Date, ISO string or epoch milliseconds
 * @param withSeconds Whether to include the seconds
 * @example formatMarketTime('2026-10-26T14:45:02Z') => '10:45:02'
 */
export function formatMarketTime(value: DateInput, withSeconds = true): string {
    return Intl.DateTimeFormat('en-US', {
        timeZone: MARKET_TIME_ZONE,
        hourCycle: 'h23',
        hour: '2-digit',
        minute: '2-digit',
        second: withSeconds ? '2-digit' : undefined,
    }).format(new Date(value));
}

/**
 * Formats a moment as a short calendar date in Eastern time
 * @param value A Date, ISO string or epoch milliseconds
 * @example formatMarketDate('2026-10-26T14:45:02Z') => 'Oct 26'
 */
export function formatMarketDate(value: DateInput): string {
    return Intl.DateTimeFormat('en-US', { timeZone: MARKET_TIME_ZONE, month: 'short', day: 'numeric' }).format(new Date(value));
}

/**
 * Gives the Eastern-time calendar day a moment falls on, for grouping things by trading day
 * @param value A Date, ISO string or epoch milliseconds
 * @example marketDayKey('2026-10-27T02:00:00Z') => '2026-10-26'
 */
export function marketDayKey(value: DateInput): string {
    // en-CA formats dates as YYYY-MM-DD
    return Intl.DateTimeFormat('en-CA', { timeZone: MARKET_TIME_ZONE, year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(value));
}