import { describe, expect, it } from 'vitest';
import { formatCurrency, formatDuration, formatMarketDate, formatMarketTime, formatNumber, formatPercent, formatPnl, formatPrice, formatSignedCurrency, formatSignedNumber, formatSignedPercent, marketDayKey, minusSign, pnlTone } from '@/lib/format';

describe('format currency', () => {
    it('should return $2,847,392 when given 2847392', () => {
        expect(formatCurrency(2847392)).toBe('$2,847,392');
    });

    it('should return $20,220,907 when given 20220907', () => {
        expect(formatCurrency(20220907)).toBe('$20,220,907');
    });
});

describe('format signed currency', () => {
    it('should return +$2,847,392 when given 2847392', () => {
        expect(formatSignedCurrency(2847392)).toBe('+$2,847,392');
    });

    it('should return -$20,220,907 when given -20220907', () => {
        expect(formatSignedCurrency(-20220907)).toBe('-$20,220,907');
    });

    it('should return $0 when given 0', () => {
        expect(formatSignedCurrency(0)).toBe('$0');
    });
});

describe('format percent', () => {
    it('should return 56% when given 0.56 and 0 digits', () => {
        expect(formatPercent(0.56, 0)).toBe('56%');
    });

    it('should return 76.5% when given 0.765 and 1 digit', () => {
        expect(formatPercent(0.765, 1)).toBe('76.5%');
    });

    it('should return -56% when given -0.56 and 0 digits', () => {
        expect(formatPercent(-0.56, 0)).toBe('-56%');
    });

    it('should throw an error when given a value greater than 1', () => {
        expect(() => formatPercent(1.01)).toThrow('Value should be between 0 and 1');
    });

    it('should throw an error when given a value less than -1', () => {
        expect(() => formatPercent(-1.01)).toThrow('Value should be between 0 and 1');
    });
});

describe('format signed percent', () => {
    it('should return +76% when given 0.76 and 0 digits', () => {
        expect(formatSignedPercent(0.76, 0)).toBe('+76%');
    });

    it('should return -56% when given -0.56 and 0 digits', () => {
        expect(formatSignedPercent(-0.56, 0)).toBe('-56%');
    });

    it('should return 0% when given 0', () => {
        expect(formatSignedPercent(0)).toBe('0%');
    });

    it('should throw an error when given a value greater than 1', () => {
        expect(() => formatSignedPercent(1.01)).toThrow('Value should be between 0 and 1');
    });

    it('should throw an error when given a value less than -1', () => {
        expect(() => formatSignedPercent(-1.01)).toThrow('Value should be between 0 and 1');
    });
});

describe('format signed number', () => {
    it('should return +907 when given 907', () => {
        expect(formatSignedNumber(907)).toBe('+907');
    });

    it('should return -907 when given -907', () => {
        expect(formatSignedNumber(-907)).toBe('-907');
    });

    it('should return 0 when given 0', () => {
        expect(formatSignedNumber(0)).toBe('0');
    });

    it('should return +2,847,392 when given 2847392', () => {
        expect(formatSignedNumber(2847392)).toBe('+2,847,392');
    });
});

describe('format price', () => {
    it('should return $5,623.50 when given 5623.5', () => {
        expect(formatPrice(5623.5)).toBe('$5,623.50');
    });

    it('should return $20.00 when given 20', () => {
        expect(formatPrice(20)).toBe('$20.00');
    });

    it('should return -$20.50 when given -20.5', () => {
        expect(formatPrice(-20.5)).toBe('-$20.50');
    });
});

describe('pnl tone', () => {
    it('should return gain when given 12', () => {
        expect(pnlTone(12)).toBe('gain');
    });

    it('should return loss when given -12', () => {
        expect(pnlTone(-12)).toBe('loss');
    });

    it('should return neutral when given 0', () => {
        expect(pnlTone(0)).toBe('neutral');
    });
});

describe('format number', () => {
    it('should return 2,871,125 when given 2871125', () => {
        expect(formatNumber(2871125)).toBe('2,871,125');
    });

    it('should return 5,623.50 when given 5623.5 and 2 digits', () => {
        expect(formatNumber(5623.5, 2)).toBe('5,623.50');
    });

    it('should return 5,621.00 when given 5621 and 2 digits', () => {
        expect(formatNumber(5621, 2)).toBe('5,621.00');
    });
});

describe('format pnl', () => {
    it('should return +$3,250 when given 3250', () => {
        expect(formatPnl(3250)).toBe('+$3,250');
    });

    it('should return -$562.50 when given -562.5', () => {
        expect(formatPnl(-562.5)).toBe('-$562.50');
    });

    it('should return $0 when given 0', () => {
        expect(formatPnl(0)).toBe('$0');
    });
});

describe('minus sign', () => {
    it('should swap a leading hyphen for a real minus sign', () => {
        expect(minusSign('-3.2%')).toBe('−3.2%');
    });

    it('should leave positive numbers alone', () => {
        expect(minusSign('+$8,234')).toBe('+$8,234');
    });

    it('should leave hyphens inside the text alone', () => {
        expect(minusSign('v2.4.1-8f2a')).toBe('v2.4.1-8f2a');
    });
});

describe('format duration', () => {
    it('should return 3d 4h for 3 days and 4 hours', () => {
        expect(formatDuration((3 * 24 + 4) * 3_600_000)).toBe('3d 4h');
    });

    it('should return 4h 12m for 4 hours and 12 minutes', () => {
        expect(formatDuration(4 * 3_600_000 + 12 * 60_000)).toBe('4h 12m');
    });

    it('should return 12m for 12 minutes and 30 seconds', () => {
        expect(formatDuration(12 * 60_000 + 30_000)).toBe('12m');
    });

    it('should return 2s for 2 seconds', () => {
        expect(formatDuration(2_000)).toBe('2s');
    });

    it('should return 0s for a negative duration', () => {
        expect(formatDuration(-5_000)).toBe('0s');
    });
});

describe('market time', () => {
    // 14:45:02 UTC is 10:45:02 in New York while daylight saving time is on
    const morning = '2026-10-26T14:45:02Z';

    it('should format the clock time in Eastern time', () => {
        expect(formatMarketTime(morning)).toBe('10:45:02');
    });

    it('should drop the seconds when asked', () => {
        expect(formatMarketTime(morning, false)).toBe('10:45');
    });

    it('should show midnight as 00, not 24', () => {
        expect(formatMarketTime('2026-10-26T04:00:00Z')).toBe('00:00:00');
    });

    it('should format the date in Eastern time', () => {
        expect(formatMarketDate(morning)).toBe('Oct 26');
    });

    it('should use the Eastern day even when UTC is already on the next day', () => {
        expect(formatMarketDate('2026-10-27T02:00:00Z')).toBe('Oct 26');
        expect(marketDayKey('2026-10-27T02:00:00Z')).toBe('2026-10-26');
    });

    it('should accept dates and epoch milliseconds too', () => {
        expect(marketDayKey(new Date(morning))).toBe('2026-10-26');
        expect(marketDayKey(Date.parse(morning))).toBe('2026-10-26');
    });
});