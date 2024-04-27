from SFI.compression.assets.encoder import *


class Decoder:
    def __init__(self):
        self.probs = []

    @staticmethod
    def binToUtf16(binstring):
        chars_bin = [binstring[i:i + 16] for i in range(0, len(binstring), 16)]

        decoded = ''
        for char in chars_bin:
            decoded += chr(int(char, 2))
        return decoded

    def decodeElias(self, encoded: str):
        """
        Performs elias gamma decoding
        :param encoded: the encoded string
        :return: Decoded number of [zeros, ones], rest of the encoded string
        """
        idx_zero = encoded.find('0')
        zeros_count = int(encoded[idx_zero + 1:2 * idx_zero + 1], 2)

        rest = encoded[2 * idx_zero + 1:]
        idx_zero = rest.find('0')

        ones_count = int(rest[idx_zero + 1:2 * idx_zero + 1], 2)

        rest = rest[2 * idx_zero + 1:]

        return [zeros_count, ones_count], rest

    def split_to_8bit(self, binstring):
        """
        Splits the binary string into 8-bit binary numbers
        
        :param binstring: The binary string
        :return: The list of 8-bit binary numbers
        """
        chars_bin = [binstring[i:i + 8] for i in range(0, len(binstring), 8)]
        return chars_bin

    def decode(self, bin_encoded):
        """
        Decodes the string produced by the Encoder class.
        :param bin_encoded: Encoded string, as binary number
        :return: List of possible answers
        """
        # Decode counts, checksum and probabilities
        counts, rest = self.decodeElias(bin_encoded)

        chars = self.split_to_8bit(rest)
        chars, checksum = chars[:-1], chars[-1]

        self.probs = Encoder.computeProbs(counts)

        # Create initial try
        # from the values set in Encoder constructor
        next_tries = [(0, MAX_RANGE, "")]

        # For every value from the output, decode it
        for single_bin in chars:
            val = int(single_bin, 2)

            current_tries = next_tries
            next_tries = []

            for _low, _range, _decoded in current_tries:
                next_tries += self._decode(val, _low, _range, _decoded)

        # Decode last character
        current_tries = next_tries
        next_tries = []
        for _low, _range, _decoded in current_tries:
            next_tries += self._decode_last(int(checksum, 2), _low, _range, _decoded)

        # Return only decoded binary values
        return [d for (l, r, d) in next_tries]

    def try_one(self, _low, _range, decoded):
        thr = (self.probs[0] * _range) >> PROB_BITS

        low_1 = _low + thr + 1
        range_1 = _range - thr - 1

        return low_1, range_1, decoded + "1"

    def try_zero(self, _low, _range, decoded):
        thr = (self.probs[0] * _range) >> PROB_BITS

        low_0 = _low
        range_0 = thr

        return low_0, range_0, decoded + "0"

    def meet_out_condition(self, _low, _range):
        return (_low & NORM_MASK) + _range <= NORM_MASK

    def update_after_output(self, _low, _range):
        _low = (_low << OUT_BITS) & STATE_MASK
        _range = ((_range << OUT_BITS) | 0xFF) & STATE_MASK

        return _low, _range

    def check_low(self, val, _low):
        return _low >> NORM_SHIFT == val

    def _decode(self, val, _low, _range, decoded):
        """
        Decode the value.

        :param val: The value from the original output, as int
        :param _low: Current `self.low`
        :param _range: Current `self.range` value
        :param decoded: Already decoded string
        :return: List of possible answers, which meet the conditions.
        """

        # Start with adding 0 and 1 to already decoded string
        q = [self.try_one(_low, _range, decoded), self.try_zero(_low, _range, decoded)]

        answers = []
        while q:
            _low, _range, decoded = q.pop(0)

            # Could not produce the output, skip it
            if self.meet_out_condition(_low, _range) and not self.check_low(val, _low):
                continue

            # Could produce output, mark as possible answer
            if self.meet_out_condition(_low, _range) and self.check_low(val, _low):
                _low, _range = self.update_after_output(_low, _range)
                answers.append((_low, _range, decoded))
                continue

            q.append(self.try_zero(_low, _range, decoded))
            q.append(self.try_one(_low, _range, decoded))

        return answers

    def has_valid_checksum(self, checksum, _low, _range):
        return (_low + _range) >> NORM_SHIFT == checksum

    def _decode_last(self, checksum, _low, _range, _decoded):
        """
        Decodes the last character. Fills up the string for the length to be divisible by 16.

        Skip all the combinations which do not produce the valid output.

        :param checksum: Checksum to perform checks
        :param _low: Current `self.low`,
        :param _range: Current `self.range`
        :param _decoded: Already decoded string
        :return:
        """

        q = [self.try_one(_low, _range, _decoded), self.try_zero(_low, _range, _decoded)]

        answers = []
        while q:
            _low, _range, decoded = q.pop(0)

            # We already processed all output characters, so it cannot be an answer
            if self.meet_out_condition(_low, _range):
                continue

            # If has valid checksum, mark it as an answer
            if len(decoded) % 16 == 0:
                if self.has_valid_checksum(checksum, _low, _range):
                    answers.append((_low, _range, decoded))
                continue

            q.append(self.try_zero(_low, _range, decoded))
            q.append(self.try_one(_low, _range, decoded))

        return answers


if __name__ == '__main__':
    answers = Decoder().decode(
        '1111111110100011110111111101110010000011001111001111101100100101000100100100000001100111100100100001111'
        '1111110111000000110010110101100011011100110010001101000111101011101000100001110100000101101100000011100'
        '11010010010010000000100011110111111011101100100100100001011101110100100000101000011100100101010100010000'
        '11100100000101101011010011010001011101111010111110001001110100111011'
    )

    for answer in answers:
        print(Decoder.binToUtf16(answer))
