import { describe, expect, it } from 'vitest';
import { formatCurrency, formatPercent, formatPrice, formatSignedCurrency, formatSignedNumber, formatSignedPercent, pnlTone } from '@/lib/format';

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