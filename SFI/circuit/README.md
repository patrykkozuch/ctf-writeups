# Circuit

## Table of contents

- [Task](#task)
- [Solution](#solution)
- [Lessons learned](#lessons-learned)

## Task

> We drew a schematic of a circuit from a mysterious device... Could you help us reverse-engineer it?
>
> Hint: The file can be opened using Logisim Evolution 3.8.0

Attachements:

- [circuit.circ](circuit.circ)

## Solution

We are given schematic drawing of an electric circuit, drawn in Logisim Evolution.

The circuit itself has five inputs and seven outputs and consist mainly OR and AND gates.

First of all, I plugged pins to inputs. They allowed me to on/off specific input by just clicking on it.

Then, I connected seven outputs to seven-segment display and tried to connect the outputs to its inputs, but couldn't
figure out the good way for it to display characters correctly.

So I tried to find some patterns and testes all combinations of the inputs:

| Input | Output  |
|-------|---------|
| 00001 | 1110011 |
| 00010 | 1100110 |
| 00011 | 1101001 |
| 00100 | 0110001 |
| 00101 | 0111001 |
| 00110 | 1011111 |
| 00111 | 1100011 |
| 01000 | 1110100 |
| 01001 | 1100110 |
| 01010 | 1111011 |
| 01011 | 1100111 |
| 01100 | 1110010 |
| 01101 | 1111010 |
| 01110 | 1101011 |
| 01111 | 1010100 |
| 10000 | 0111101 |
| 10001 | 0111001 |
| 10010 | 0111100 |
| 10011 | 1111101 |

After first 20 tries, all next tries were zero-ed on outputs. So I started to think, what this output can mean.
Out of curiosity, I tried to decode outputs as binary numbers and... it worked!

I treated the output as 8-bit binary numbers and decoding them
through [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Binary('Space',8)&input=MDExMTAwMTENCjAxMTAwMTEwDQowMTEwMTAwMQ0KMDAxMTAwMDENCjAwMTExMDAxDQowMTAxMTExMQ0KMDExMDAwMTENCjAxMTEwMTAwDQowMTEwMDExMA0KMDExMTEwMTENCjAxMTAwMTExDQowMTExMDAxMA0KMDExMTEwMTANCjAxMTAxMDExDQowMTAxMDEwMA0KMDAxMTExMDENCjAwMTExMDAxDQowMDExMTEwMA0KMDExMTExMDENCg&ieol=CRLF&oeol=CR)
I got the flag:

Flag: **_sfi19_ctf{grzkT=9<}_**

## Lessons learned:

- If you don't know how to proceed, first gather all information possible
- Trust your intuition
