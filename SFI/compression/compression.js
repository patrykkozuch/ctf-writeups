STATE_BITS = 24;
STATE_MASK = (1 << STATE_BITS) - 1;
PROB_BITS = 8;
MAX_RANGE = (1 << STATE_BITS) - 1;
OUT_BITS = 8;
NORM_SHIFT = STATE_BITS - OUT_BITS;
NORM_MASK = (1 << NORM_SHIFT) - 1;

class Encoder {
    constructor() {
        this.low = 0;
        this.range = MAX_RANGE;
    }

    elias(value) {
        var value_bin = value.toString(2)
        return "1".repeat(value_bin.length) + "0" + value_bin
    }

    getCounts(string) {
        return string.split('').reduce(([a, b], x) => (x == '1' ? [a, b + 1] : [a + 1, b]), [0, 0]);
    }

    computeProbs(counts) {
        var total = counts.reduce((a, b) => a + b);
        var probs = [];
        for (var v of counts) {
            probs.push(Math.floor((v << PROB_BITS) / total));
        }
        // fill rounding errors
        var sum = probs.reduce((a, b) => a + b);
        probs[0] += ((1 << PROB_BITS) - sum);
        return probs;
    }

    utf16ToBin(val) {
        return val.toString(2).padStart(16, '0');
    }

    valToBin(val) {
        return val.toString(2).padStart(8, '0');
    }

    valToHex(val) {
        return val.toString(16).padStart(2, '0');
    }

    strToBin(string) {
        var bin_string = "";
        for (let idx = 0; idx < string.length; ++idx) {
            let v = this.utf16ToBin(string.charCodeAt(idx));
            bin_string += v;
        }
        return bin_string;
    }

    encodeBit(bit, probab) {
        var thr = (probab * this.range) >>> PROB_BITS;

        if (bit) {
            this.low += thr + 1;
            this.range -= thr + 1;
        } else {
            this.range = thr;
        }
    }

    encode(text) {
        var bin_text = this.strToBin(text);
        var counts = this.getCounts(bin_text)
        var probs = this.computeProbs(counts);

        var code = "";
        for (var bit_s of bin_text) {
            var bit = (bit_s == '1');
            this.encodeBit(bit, probs[0]);
            if ((this.low & NORM_MASK) + this.range <= NORM_MASK) {
                var to_write = this.low >>> NORM_SHIFT;
                code += this.valToBin(to_write);

                this.low = (this.low << OUT_BITS) & STATE_MASK;
                this.range = ((this.range << OUT_BITS) | 0xFF) & STATE_MASK;
            }
        }
        var to_write = (this.low + this.range) >>> NORM_SHIFT;
        code += this.valToBin(to_write);

        var counts_enc = counts.map(this.elias)
        var encoded = counts_enc.join('') + code;
        return encoded;
    }
}

function encode() {
    var text = document.querySelector("#plain_text").value;
    var enc = new Encoder();
    var encoded = enc.encode(text);
    document.querySelector("#response").innerHTML = encoded;

    var msg = "";
    for (var i = 0; i < encoded.length; i += 8) {
        var x = encoded.substring(i, i+8).padEnd(8, "0");
        msg += parseInt(x, 2).toString(16).padStart(2, "0");
    }
    console.log(msg)
}

// sfi_19{this_is_flag}
// 111111110111001011111111010110110000110011110011111011001001010001001001000000111110110100010010100000101111001111001010011111000000000100100011101010111110010000000010101111110100110100000101000000111100001110010111010110100100011001111110100101100111001010001011010000100101100011000110001100110010111000101101
// ff72ff5b0cf3ec944903ed1282f3ca7c0123abe402bf4d0503c3975a467e96728b4258c6332e2d