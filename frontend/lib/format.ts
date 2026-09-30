/**
 * Formats a number to USD
 * @param value  The amount of money
 * @example formatCurrency(2847392) => $2,847,392
 */
export function formatCurrency(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(value);
}

/**
 * Formats a number to USD with a + or - in front
 * @param value  The amount of money
 * @example formatSignedCurrency(2847392) => +$2,847,392
 */
export function formatSignedCurrency(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0, signDisplay: 'exceptZero' }).format(value);
}

/**
 * Formats a decimal to a percentage
 * @param value The decimal to format
 * @param digits How many decimal places to have
 * @example formatPercent(0.56, 0) => 56% 
 */
export function formatPercent(value: number, digits = 1): string {
    if (value > 1 || value < -1) throw new Error('Value should be between 0 and 1');

    return Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: digits, signDisplay: 'negative' }).format(value);
}

/**
 * Formats a decimal to a percentage
 * @param value The decimal to format
 * @param digits How many decimal places to have
 * @example formatSignedPercent(0.76) => +76%
 */
export function formatSignedPercent(value: number, digits = 1): string {
    if (value > 1 || value < -1) throw new Error('Value should be between 0 and 1');

    return Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: digits, signDisplay: 'exceptZero' }).format(value);
}

/**
 * Formats a number with either + or - in front
 * @param value The number to format
 * @example formatSignedNumber(907) => +907
 */
export function formatSignedNumber(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'decimal', signDisplay: 'exceptZero', maximumFractionDigits: 0 }).format(value);
}

/**
 * Formats a price to include the two decimal places
 * @param value The number to format
 * @example formatPrice(5623.5) => 5623.50
 */
export function formatPrice(value: number): string {
    return Intl.NumberFormat('en-US', { style: 'currency', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
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