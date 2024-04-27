import math

STATE_BITS = 24
STATE_MASK = (1 << STATE_BITS) - 1
PROB_BITS = 8
MAX_RANGE = (1 << STATE_BITS) - 1
OUT_BITS = 8
NORM_SHIFT = STATE_BITS - OUT_BITS
NORM_MASK = (1 << NORM_SHIFT) - 1


class Encoder:
    def __init__(self):
        self.low = 0
        self.range = MAX_RANGE

    def elias(self, value):
        value_bin = bin(value)[2:]
        return "1" * len(value_bin) + "0" + value_bin

    def getCounts(self, string):
        return [string.count('0'), string.count('1')]

    @staticmethod
    def computeProbs(counts):
        total = sum(counts)
        probs = [math.floor((v << PROB_BITS) / total) for v in counts]
        # fill rounding errors
        sum_probs = sum(probs)
        probs[0] += ((1 << PROB_BITS) - sum_probs)
        return probs

    def utf16ToBin(self, val):
        return format(val, '016b')

    def valToBin(self, val):
        return format(val, '08b')

    def valToHex(self, val):
        return format(val, '02x')

    def strToBin(self, string):
        return ''.join([self.utf16ToBin(ord(c)) for c in string])

    def encodeBit(self, bit, probab):
        thr = (probab * self.range) >> PROB_BITS
        if bit:
            self.low += thr + 1
            self.range -= thr + 1
        else:
            self.range = thr

    def encode(self, text):
        # Transform text to its binary representation
        bin_text = self.strToBin(text)
        # Get counts of 0's and 1's
        counts = self.getCounts(bin_text)
        # Get the probabilities
        probs = self.computeProbs(counts)

        code = ""
        # For every bit
        for bit_s in bin_text:
            bit = (bit_s == '1')
            # Encode it
            self.encodeBit(bit, probs[0])

            # Write the `low` as a binary output if conditions are met
            # (don't care about exact values)
            if (self.low & NORM_MASK) + self.range <= NORM_MASK:
                to_write = self.low >> NORM_SHIFT
                code += self.valToBin(to_write)

                # Update the low and range (don't care about exact values)
                self.low = (self.low << OUT_BITS) & STATE_MASK
                self.range = ((self.range << OUT_BITS) | 0xFF) & STATE_MASK

        # Write the checksum to the ouput as a binary number
        to_write = (self.low + self.range) >> NORM_SHIFT
        code += self.valToBin(to_write)

        # Write counts as elias encoded at THE BEGINNING of the output
        counts_enc = [self.elias(c) for c in counts]
        encoded = ''.join(counts_enc) + code
        return encoded